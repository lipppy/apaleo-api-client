from datetime import datetime, timedelta
from typing import Optional

import anyio.lowlevel
import httpx

from apaleoapi.constants import APALEO_API_TOKEN_URL
from apaleoapi.logging import get_logger
from apaleoapi.ports.http.auth import TokenProviderPort

log = get_logger(__name__)


class BaseTokenProvider(TokenProviderPort):
    """Common implementation + safe defaults."""

    def __init__(self, service: str, type_: str) -> None:
        self._service = service
        self._type = type_
        self._token: str | None = None
        self._refresh_token: str | None = None  # For auth code flow
        self._token_expiry: datetime | None = None  # Optional expiry tracking

    async def get_token(self, is_new: bool = False) -> str | None:
        """Get the current access token, refreshing it if necessary."""
        log.debug(f"Getting token for {self._service} (is_new={is_new}).")

        # Check if token is expired before using it
        if self._token and self._token_expiry and datetime.now() >= self._token_expiry:
            log.debug("Token expired, forcing refresh.")
            is_new = True

        if not self._token or is_new:
            log.debug(f"Fetching new {self._type} token for {self._service}.")
            await self.refresh_token()
        else:
            log.debug(f"Using cached {self._type} token for {self._service}.")
        return self._token

    async def auth_header(self, is_new: bool = False) -> dict[str, str]:
        log.debug(f"Getting auth header for {self._service} (is_new={is_new}).")
        token = await self.get_token(is_new=is_new)
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    async def refresh_token(self) -> None:
        """To be implemented by concrete providers."""
        raise NotImplementedError

    async def close(self) -> None:
        """Default no-op close."""
        log.debug(f"No-op close for token provider {self._service}.")
        # No resources to close by default
        await anyio.lowlevel.checkpoint()


class OAuth2ClientCredentialsProvider(BaseTokenProvider):
    _type: str = "OAuth2ClientCredentials"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        service: str,
        token_url: str = APALEO_API_TOKEN_URL,
        scope: Optional[str] = None,
        audience: Optional[str] = None,
        extra: Optional[dict[str, str]] = None,
        timeout: int = 10,
    ):
        super().__init__(service, self._type)
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.audience = audience
        self.extra = extra or {}
        self.timeout = timeout

    async def refresh_token(self) -> None:
        """Refresh the access token by authenticating with the token endpoint."""
        async with httpx.AsyncClient(timeout=self.timeout, verify=True) as client:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                **self.extra,
            }
            if self.scope:
                data["scope"] = self.scope
            if self.audience:
                data["audience"] = self.audience
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = await client.post(self.token_url, data=data, headers=headers)
            if resp.status_code != 200:
                log.warning(f"Authentication failed with status {resp.status_code}.")
                raise RuntimeError("Authentication failed. Please check your credentials.")
            self._token = resp.json().get("access_token")
            if not self._token:
                raise RuntimeError("Auth failed: no access_token")
            log.debug("Token refreshed.")


class OAuth2AuthorizationCodeProvider(BaseTokenProvider):
    _type: str = "OAuth2AuthorizationCode"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        service: str,
        redirect_uri: str,
        token_url: str = APALEO_API_TOKEN_URL,
        scope: Optional[str] = None,
        audience: Optional[str] = None,
        extra: Optional[dict[str, str]] = None,
        timeout: int = 10,
    ):
        super().__init__(service, self._type)
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.audience = audience
        self.extra = extra or {}
        self.timeout = timeout

    async def refresh_token(self) -> None:
        """Refresh the access token by exchanging the authorization code or refresh token."""
        async with httpx.AsyncClient(timeout=self.timeout, verify=True) as client:
            if not self._token:
                log.debug("Exchanging authorization code for access token...")
                # First time: exchange authorization code for token
                data = {
                    "grant_type": "authorization_code",
                    "code": self.extra.get("authorization_code"),
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }
            else:
                # Subsequent times: use refresh token
                log.debug("Refreshing access token using refresh token...")
                data = {
                    "grant_type": "refresh_token",
                    "refresh_token": self._refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }
            if self.scope:
                data["scope"] = self.scope
            if self.audience:
                data["audience"] = self.audience
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = await client.post(self.token_url, data=data, headers=headers)
            if resp.status_code != 200:
                log.warning(f"Authentication failed with status {resp.status_code}")
                raise RuntimeError("Authentication failed. Please check your credentials.")
            json_resp = resp.json()
            self._token = json_resp.get("access_token")
            if not self._token:
                raise RuntimeError("Auth failed: no access_token")
            # Update refresh token if provided
            if new_refresh_token := json_resp.get("refresh_token"):
                self._refresh_token = new_refresh_token
                log.debug("Refresh token updated.")
            # Optionally handle token expiry if provided by the auth server (e.g., expires_in)
            if expires_in := json_resp.get("expires_in"):
                self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
                log.debug(f"Token expiry set to {self._token_expiry}.")

            log.debug("Token refreshed.")
