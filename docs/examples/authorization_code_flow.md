# Authorization Code Flow Example

This example demonstrates how to use the Apaleo API Client with the OAuth2 Authorization Code flow. This flow is ideal for applications that need to access resources on behalf of a user.

```python {title="Minimal example using the Authorization Code flow"}
import secrets
import urllib.parse
from dataclasses import asdict
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from apaleoapi import ApaleoAPIClient, OAuth2AuthorizationCodeProvider
from apaleoapi.constants import APALEO_API_AUTHORIZE_URL


app = FastAPI("Apaleo OAuth2 Authorization Code Flow Demo")
CLIENT_ID, CLIENT_SECRET = "your-client-id", "your-client-secret"
REDIRECT_URI = "http://localhost:8000/callback"
auth_states, api_client = {}, None


@app.get("/")
async def index() -> HTMLResponse:
    state = secrets.token_urlsafe(16)
    auth_states[state] = True
    auth_url = f"{APALEO_API_AUTHORIZE_URL}?{
        urllib.parse.urlencode(
            {
                'response_type': 'code',
                'client_id': CLIENT_ID,
                'redirect_uri': REDIRECT_URI,
                'state': state,
                'scope': 'openid profile offline_access identity:account-users.read',
            }
        )
    }"
    return HTMLResponse(f'<a href="{auth_url}">Start OAuth2 Authorization</a>')


@app.get("/callback")
async def callback(code: str = Query(), state: str = Query()) -> dict[str, Any]:
    global api_client
    if state not in auth_states:
        return {"error": "Invalid state"}
    del auth_states[state]

    token_provider = OAuth2AuthorizationCodeProvider(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        service="Apaleo API Client - Authorization Code Flow",
        redirect_uri=REDIRECT_URI,
        extra={"authorization_code": code},
    )
    await token_provider.refresh_token()
    api_client = ApaleoAPIClient(token_provider=token_provider)
    return {"success": True, "message": "Authenticated! Visit http://localhost:8000/identity"}


@app.get("/identity")
async def get_identity() -> dict[str, Any]:
    user = await api_client.identity.v1.identity.get_current_user()
    return asdict(user)


if __name__ == "__main__":
    print("🚀 Apaleo OAuth2 Authorization Code Flow Demo")
    print(f"📱 Client ID: {CLIENT_ID}")
    print(f"🔗 Redirect URI: {REDIRECT_URI}")
    print()
    print(
        "Run with: poetry run python -m uvicorn path_to_your_module:app --host 0.0.0.0 --port 8000 --reload"
    )
    print("Navigate to: http://localhost:8000")
```
