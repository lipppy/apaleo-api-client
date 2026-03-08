# Apaleo API Authorization Code Test

This directory contains a lightweight FastAPI application for testing the OAuth2 Authorization Code flow with the Apaleo API.

## Features

- **Index Page**: Displays OAuth2 configuration and provides a link to start the authorization flow
- **Callback Page**: Handles the authorization code callback from Apaleo and exchanges it for an access token
- **Health Check**: Simple health endpoint for monitoring
- **CSRF Protection**: Uses state parameter to prevent CSRF attacks
- **Error Handling**: Comprehensive error handling for various failure scenarios

## Setup

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Set Environment Variables**:
   ```bash
   export APALEO_CLIENT_ID="your-actual-client-id"
   export APALEO_CLIENT_SECRET="your-actual-client-secret"
   export REDIRECT_URI="http://localhost:8000/callback"
   export BASE_URL="http://localhost:8000"
   ```

3. **Configure Apaleo OAuth2 App**:
   - Go to your Apaleo developer console
   - Create or configure your OAuth2 application
   - Set the redirect URI to `http://localhost:8000/callback`
   - Note down your client ID and client secret

## Usage

### Method 1: Run directly (with auto-reload)
```bash
python test_authorization_code.py
```

### Method 2: Run with uvicorn command (recommended for development)
```bash
# Basic uvicorn with auto-reload
uvicorn test_authorization_code:app --host 0.0.0.0 --port 8000 --reload

# With more verbose logging
uvicorn test_authorization_code:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Method 3: Run with Poetry
```bash
poetry run python test_authorization_code.py
```

**Note**: Auto-reload is enabled by default. The server will automatically restart when you make changes to the code.

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Follow the OAuth2 flow**:
   - Click "Start Authorization"
   - Log in with your Apaleo credentials
   - Grant permissions to the application
   - You'll be redirected back with the results

## API Endpoints

- `GET /` - Main index page with authorization link
- `GET /callback` - OAuth2 callback endpoint
- `GET /health` - Health check endpoint

## Configuration

The application uses the following scopes by default:
- `openid`
- `profile`
- `offline_access`
- `setup:property.read`
- `availability:rates.read`
- `reservations:reservations.read`
- `inventory:inventory.read`

You can modify the `SCOPES` list in the code to adjust permissions as needed.

## Integration with apaleo-api-client

The app demonstrates how to use the `OAuth2AuthorizationCodeProvider` from the main apaleo-api-client library:

```python
from apaleoapi.http.auth import OAuth2AuthorizationCodeProvider
from apaleoapi.constants import APALEO_API_TOKEN_URL, APALEO_API_AUTHORIZE_URL

# Create provider with authorization code
token_provider = OAuth2AuthorizationCodeProvider(
    token_url=APALEO_API_TOKEN_URL,
    authorize_url=APALEO_API_AUTHORIZE_URL,
    redirect_uri="http://localhost:8000/callback",
    client_id="your-client-id",
    client_secret="your-client-secret",
    service="Your App Name",
    extra={"authorization_code": code}
)

# Exchange code for token
await token_provider.refresh_token()
token = await token_provider.get_token()
```

## Security Notes

- The app includes CSRF protection using state parameters
- Client secrets should be kept secure and not exposed in client-side code
- For production use, implement proper session management instead of in-memory state storage
- Use HTTPS in production environments
