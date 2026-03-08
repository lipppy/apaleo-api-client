"""
FastAPI app for testing Apaleo API OAuth2 Authorization Code flow.

This lightweight web application demonstrates how to implement the OAuth2 authorization
code flow for the Apaleo API using the apaleo-api-client library.
"""

import logging
import secrets
import urllib.parse
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Optional

from dotenv import dotenv_values
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse

from apaleoapi.client import ApaleoAPIClient
from apaleoapi.constants import APALEO_API_AUTHORIZE_URL
from apaleoapi.http.auth import OAuth2AuthorizationCodeProvider

# Load environment variables from .env file
config = dotenv_values(".env.authorization_code")  # Load from specific .env file for this test

# Logging configuration
log_level = config.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s | %(levelname)8s | %(message)s",
)
log = logging.getLogger(__name__)


# FastAPI app instance
app = FastAPI(
    title="Apaleo API Authorization Code Test",
    description="Test application for Apaleo OAuth2 Authorization Code flow",
    version="1.0.0",
)

# Configuration - You should set these as environment variables
CLIENT_ID = config.get("APALEO_CLIENT_ID")
CLIENT_SECRET = config.get("APALEO_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "Missing required environment variables: APALEO_CLIENT_ID and APALEO_CLIENT_SECRET"
    )

REDIRECT_URI = "http://localhost:8000/callback"
BASE_URL = "http://localhost:8000"

# Scopes for Apaleo API - adjust based on your needs
SCOPES = ["openid", "profile", "offline_access", "identity:account-users.read"]


# Secure state management with expiration and cleanup
class SecureStateManager:
    def __init__(self, max_states: int = 100, expiry_minutes: int = 10):
        self._states = {}
        self.max_states = max_states
        self.expiry_minutes = expiry_minutes

    def add_state(self, state: str) -> None:
        # Cleanup expired states
        self._cleanup_expired()
        # Enforce size limits
        if len(self._states) >= self.max_states:
            # Remove oldest state
            oldest = min(self._states.keys(), key=lambda k: self._states[k])
            del self._states[oldest]

        self._states[state] = datetime.now()

    def validate_and_remove(self, state: str) -> bool:
        if state not in self._states:
            return False

        # Check if expired
        if datetime.now() - self._states[state] > timedelta(minutes=self.expiry_minutes):
            del self._states[state]
            return False

        # Valid state, remove it
        del self._states[state]
        return True

    def _cleanup_expired(self) -> None:
        now = datetime.now()
        expired = [
            k for k, v in self._states.items() if now - v > timedelta(minutes=self.expiry_minutes)
        ]
        for k in expired:
            del self._states[k]


auth_states = SecureStateManager()

# Store the authenticated client after successful authorization
authenticated_client = None

LINK_FAVICON = """
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>" />
"""

# HTML templates
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Apaleo API Authorization Test</title>
    {link_favicon}
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .btn {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 10px 0;
        }}
        .btn:hover {{ background-color: #0056b3; }}
        .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .error {{ background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .success {{ background-color: #d4edda; color: #155724; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .code {{ background-color: #f8f9fa; padding: 10px; font-family: monospace; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Apaleo API Authorization Code Test</h1>

        <div class="info">
            <h3>Configuration</h3>
            <p><strong>Client ID:</strong> {client_id}</p>
            <p><strong>Redirect URI:</strong> {redirect_uri}</p>
            <p><strong>Scopes:</strong> {scopes}</p>
        </div>

        <div class="info">
            <h3>OAuth2 Authorization Code Flow</h3>
            <p>This demo shows how to implement the OAuth2 Authorization Code flow with the Apaleo API.</p>
            <ol>
                <li>Click the "Start Authorization" button below</li>
                <li>You'll be redirected to Apaleo's authorization server</li>
                <li>Log in with your Apaleo credentials</li>
                <li>Grant permissions to this application</li>
                <li>You'll be redirected back with an authorization code</li>
                <li>The code will be exchanged for an access token</li>
            </ol>
        </div>

        <a href="{auth_url}" class="btn">Start Authorization</a>

        <div class="info">
            <h3>Environment Setup</h3>
            <p>Make sure to set the following environment variables:</p>
            <div class="code">
APALEO_CLIENT_ID=your-actual-client-id<br>
APALEO_CLIENT_SECRET=your-actual-client-secret<br>
REDIRECT_URI=http://localhost:8000/callback<br>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Success callback template
SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Authorization Result - Apaleo API</title>
    {link_favicon}
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .btn {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 10px 0;
        }}
        .btn:hover {{ background-color: #0056b3; }}
        .success {{ background-color: #d4edda; color: #155724; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .code {{ background-color: #f8f9fa; padding: 10px; font-family: monospace; border-radius: 4px; word-break: break-all; }}
        .token-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Authorization Result</h1>
        <div class="success">
            <h3>✅ Authorization Successful!</h3>
            <p>Successfully obtained access token from Apaleo API.</p>
        </div>

        <div class="token-info">
            <h3>Token Information</h3>
            <p><strong>Access Token (first 20 chars):</strong> <span class="code">{token_preview}...</span></p>
            <p><strong>Token Type:</strong> Bearer</p>
            <p><strong>API Ready:</strong> ✅ Yes</p>
        </div>

        <div class="token-info">
            <h3>Next Steps</h3>
            <p>You can now use this token to make authenticated requests to the Apaleo API:</p>
            <p><strong>Test the API:</strong> <a href="/identity" target="_blank">/identity</a> - Get current user info</p>
            <p><strong>Debug Token:</strong> <a href="/debug-token" target="_blank">/debug-token</a> - Check token status</p>
            <p><strong>Health Check:</strong> <a href="/health" target="_blank">/health</a> - Check server health</p>
            <div class="code">
# Example usage with apaleo-api-client<br>
from apaleoapi.http.auth import OAuth2AuthorizationCodeProvider<br>
from apaleoapi.http.transport import AuthenticatedTransport<br><br>
# The provider now has a valid token<br>
transport = AuthenticatedTransport(<br>
&nbsp;&nbsp;&nbsp;&nbsp;base_url="https://api.apaleo.com/",<br>
&nbsp;&nbsp;&nbsp;&nbsp;token_provider=your_token_provider<br>
)
            </div>
        </div>

        <a href="/" class="btn">Start Over</a>
    </div>
</body>
</html>
"""

# Error callback template
ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Authorization Result - Apaleo API</title>
    {link_favicon}
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .btn {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 10px 0;
        }}
        .btn:hover {{ background-color: #0056b3; }}
        .error {{ background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 4px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Authorization Result</h1>
        <div class="error">
            <h3>❌ Authorization Failed</h3>
            <p>{error_message}</p>
            {error_details_section}
        </div>
        <a href="/" class="btn">Start Over</a>
    </div>
</body>
</html>
"""


# Global state - in production use proper session/database storage
apaleo_api_client: Optional[ApaleoAPIClient] = None
token_provider: Optional[OAuth2AuthorizationCodeProvider] = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """
    Main index page - displays authorization information and start button.
    """
    # Generate a random state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    auth_states.add_state(state)

    # Build authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": state,
    }

    auth_url = f"{APALEO_API_AUTHORIZE_URL}?{urllib.parse.urlencode(auth_params)}"

    return HTMLResponse(
        INDEX_TEMPLATE.format(
            link_favicon=LINK_FAVICON,
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            scopes=", ".join(SCOPES),
            auth_url=auth_url,
        )
    )


@app.get("/callback")
async def callback(
    request: Request,
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_description: Optional[str] = Query(None),
) -> HTMLResponse:
    """
    OAuth2 callback endpoint - handles the authorization code from Apaleo.

    Args:
        code: Authorization code from Apaleo
        state: State parameter for CSRF protection
        error: Error code if authorization failed
        error_description: Human-readable error description
    """
    # Check for authorization errors
    if error:
        error_msg = f"Authorization failed: {error}"
        if error_description:
            error_msg += f" - {error_description}"

        error_details_section = (
            f"<p><strong>Details:</strong> {error_description}</p>" if error_description else ""
        )

        return HTMLResponse(
            ERROR_TEMPLATE.format(
                link_favicon=LINK_FAVICON,
                error_message=error_msg,
                error_details_section=error_details_section,
            )
        )

    # Validate state parameter
    if not state or not auth_states.validate_and_remove(state):
        return HTMLResponse(
            ERROR_TEMPLATE.format(
                link_favicon=LINK_FAVICON,
                error_message="Invalid or expired state parameter - possible CSRF attack or expired session",
                error_details_section="",
            )
        )

    # Validate authorization code
    if not code:
        return HTMLResponse(
            ERROR_TEMPLATE.format(
                link_favicon=LINK_FAVICON,
                error_message="No authorization code received",
                error_details_section="",
            )
        )

    try:
        # Create OAuth2 provider with the authorization code
        token_provider = OAuth2AuthorizationCodeProvider(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            service="Apaleo API Test App",
            redirect_uri=REDIRECT_URI,
            scope=" ".join(SCOPES),
            extra={"authorization_code": code},
        )

        # Exchange authorization code for access token
        await token_provider.refresh_token()

        # Verify we got a token
        token = await token_provider.get_token()
        if not token:
            raise ValueError("Failed to obtain access token")

        # Success - show token information
        token_preview = token[:20] if len(token) > 20 else token

        global authenticated_client
        authenticated_client = ApaleoAPIClient(token_provider=token_provider)

        return HTMLResponse(
            SUCCESS_TEMPLATE.format(link_favicon=LINK_FAVICON, token_preview=token_preview)
        )

    except Exception as e:
        # Handle token exchange errors
        error_details_section = f"<p><strong>Details:</strong> {str(e)}</p>"

        return HTMLResponse(
            ERROR_TEMPLATE.format(
                link_favicon=LINK_FAVICON,
                error_message="Failed to exchange authorization code for token",
                error_details_section=error_details_section,
            )
        )


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """
    Simple health check endpoint.
    """
    global authenticated_client
    return {
        "status": "healthy",
        "service": "apaleo-api-auth-test",
        "authenticated": authenticated_client is not None,
        "endpoints": {
            "index": "/",
            "callback": "/callback",
            "health": "/health",
            "identity": "/identity",
            "debug-token": "/debug-token",
        },
    }


@app.get("/identity")
async def test_identity() -> dict[str, Any]:
    """
    Test endpoint to call Apaleo Identity API using the obtained token.
    """
    global authenticated_client

    if not authenticated_client:
        return {
            "error": "No authenticated client available. Please complete authorization flow first.",
            "instructions": "Visit / to start authorization, then come back to /identity",
        }

    try:
        invitations = await authenticated_client.identity.v1.identity.list_invitations()
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to call Identity API: {str(e)}",
            "details": "This could be due to insufficient scopes or expired token",
            "error_type": type(e).__name__,
        }

    try:
        users = await authenticated_client.identity.v1.identity.list_users()
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to call Identity API: {str(e)}",
            "details": "This could be due to insufficient scopes or expired token",
            "error_type": type(e).__name__,
        }

    try:
        current_user = await authenticated_client.identity.v1.identity.get_current_user()
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to call Identity API: {str(e)}",
            "details": "This could be due to insufficient scopes or expired token",
            "error_type": type(e).__name__,
        }

    return {
        "success": True,
        "invitations": asdict(invitations),
        "users": asdict(users),
        "current_user": asdict(current_user),
    }


@app.get("/debug-token")
async def debug_token() -> dict[str, Any]:
    """
    Debug endpoint to check token status.
    """
    global authenticated_client

    if not authenticated_client:
        return {"authenticated": False, "message": "No authenticated client available"}

    try:
        # Try to get the token to check if it's valid and can be refreshed if needed
        token = await authenticated_client.token_provider.get_token()

        return {
            "authenticated": True,
            "token_available": token is not None,
            "token_preview": token[:20] + "..." if token else None,
            "provider_type": type(authenticated_client.token_provider).__name__,
        }
    except Exception as e:
        return {"authenticated": True, "error": str(e), "error_type": type(e).__name__}


if __name__ == "__main__":
    print("🚀 Starting Apaleo API Authorization Code Test Server")
    print(f"📱 Client ID: {CLIENT_ID}")
    print(f"🔗 Redirect URI: {REDIRECT_URI}")
    print(f"🌐 Server URL: {BASE_URL}")
    print(f"📋 Scopes: {', '.join(SCOPES)}")
    print()
    print("🔧 Make sure to set your environment variables:")
    print("    APALEO_CLIENT_ID=your-actual-client-id")
    print("    APALEO_CLIENT_SECRET=your-actual-client-secret")
    print("    REDIRECT_URI=http://localhost:8000/callback")
    print()
    print("📖 Navigate to http://localhost:8000 to start the authorization flow.")
    print("🔄 For auto-reload during development, use:")
    print(
        "    poetry run python -m uvicorn test_authorization_code:app --host 0.0.0.0 --port 8000 --reload"
    )
