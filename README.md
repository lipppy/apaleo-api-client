# Apaleo API Client

[![CI](https://img.shields.io/github/actions/workflow/status/lipppy/apaleo-api-client/tests.yml?branch=main&logo=github&label=CI)](https://github.com/lipppy/apaleo-api-client/actions?query=event%3Apush+branch%3Amain+workflow%3ATests)
[![Coverage](https://codecov.io/github/lipppy/apaleo-api-client/coverage.svg)](https://codecov.io/github/lipppy/apaleo-api-client)
[![pypi](https://img.shields.io/pypi/v/apaleo-api-client.svg)](https://pypi.python.org/pypi/apaleo-api-client)
[![downloads](https://static.pepy.tech/badge/apaleo-api-client/month)](https://pepy.tech/project/apaleo-api-client)
[![versions](https://img.shields.io/pypi/pyversions/apaleo-api-client.svg)](https://github.com/lipppy/apaleo-api-client/blob/main/pyproject.toml#L15)
[![license](https://img.shields.io/github/license/lipppy/apaleo-api-client.svg)](https://github.com/lipppy/apaleo-api-client/blob/main/LICENSE)

Python SDK for the Apaleo API. Provides a type-safe, async client for seamless integration with Apaleo's hospitality platform. Built on Pydantic v2 and httpx. Fast, easy to use, and fully documented.

## Help

See [documentation](https://lipppy.github.io/apaleo-api-client/) for more details.

## Features

This SDK is actively under development with the goal of providing full coverage of the Apaleo API Swagger specifications focusing on `v1` but with the capability and intention to expand to other versions in the future.

Current status:

- **Type-safe abstractions** - Full type hints and Pydantic models for implemented resources
- **Async/await support** - Non-blocking I/O for high-performance applications
- **Authentication handling** - Built-in support for OAuth 2.0 flows (Client Credentials, Authorization Code)
- **Integration-tested** - Implemented endpoints validated against a DEV instance
- **Documentation-first** - Usage examples and docs evolving alongside feature coverage

## Installation

Install using `pip install -U apaleo-api-client` or `poetry add apaleo-api-client`.
For more installation options to make Apaleo API Client even faster,
see the [Installation](https://lipppy.github.io/apaleo-api-client/main/install/) section in the documentation.

## Code Examples

- [OAuth 2.0 - Client credentials grant flow](https://apaleo.dev/guides/oauth-connection/simple-client.html)
- [OAuth 2.0 - Authorization code grant flow](https://apaleo.dev/guides/oauth-connection/auth-code-grant.html)

### Client Credentials

```python
from apaleoapi import ApaleoAPIClient
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider

# Create a token provider with your API credentials
token_provider = OAuth2ClientCredentialsProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    service="Apaleo API Client - Client Credentials Flow"
)

# Create an instance of the client
client = ApaleoAPIClient(token_provider=token_provider)

# Fetch a property by its ID
property_berlin = await client.core.v1.inventory.get_property(property_id="BER")
print(property_berlin)
#> Property id=BER name='Berlin Hotel' address='123 Berlin St.'
print(type(property_berlin))
#> <class 'apaleo_api_client.core.v1.inventory.Property'>

print(property_berlin.id)
#> BER
```

### Authorization Code (FastAPI)

In production, you should use proper session/database storage for the `state` parameter and token management. This example is simplified for demonstration purposes.

```python
import secrets
import urllib.parse
from dataclasses import asdict
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from apaleoapi import ApaleoAPIClient
from apaleoapi.constants import APALEO_API_AUTHORIZE_URL
from apaleoapi.http.auth import OAuth2AuthorizationCodeProvider

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

## Contributing

For guidance on setting up a development environment and how to make a
contribution to Apaleo API Client, see
[Contributing to Apaleo API Client](https://docs.pydantic.dev/contributing/).

## Reporting a Security Vulnerability

See our [security policy](https://github.com/pydantic/pydantic/security/policy).

## About the Author

This SDK was created to provide modern, type-safe Python bindings for the Apaleo API. The author has a background in meteorology and hydrology with 10+ years of full-stack web development and 5+ years specializing in Python. Currently working in the hospitality domain and actively integrating with Apaleo APIs, this project began as a way to eliminate repetitive API implementation work and provide Python developers with a robust, production-ready SDK.

This is the author's first library published on PyPI. As a hobby project, support and development pace depend on availability beyond work commitments.
