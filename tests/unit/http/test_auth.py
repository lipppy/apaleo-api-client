from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from apaleoapi.http.auth import (
    BaseTokenProvider,
    OAuth2AuthorizationCodeProvider,
    OAuth2ClientCredentialsProvider,
)

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


class TestBaseTokenProvider:
    """Tests for the BaseTokenProvider class, which provides common token management logic."""

    class DummyTokenProvider(BaseTokenProvider):
        """A simple token provider for testing the base class behavior."""

        def __init__(self) -> None:
            super().__init__(service="test-service", type_="Dummy")
            self.refresh_calls = 0
            self.next_token: str | None = "new-token"

        async def refresh_token(self) -> None:
            self.refresh_calls += 1
            self._token = self.next_token

    async def test_get_token_refreshes_when_missing(self) -> None:
        """Test that get_token calls refresh_token when no token is available."""
        provider = self.DummyTokenProvider()

        token = await provider.get_token()

        assert provider.refresh_calls == 1
        assert token == "new-token"

    async def test_get_token_uses_cached_token(self) -> None:
        """Test that get_token returns the cached token when it is still valid."""
        provider = self.DummyTokenProvider()
        provider._token = "cached-token"
        provider._token_expiry = datetime.now() + timedelta(minutes=5)

        token = await provider.get_token()

        assert provider.refresh_calls == 0
        assert token == "cached-token"

    async def test_get_token_forces_refresh_when_is_new(self) -> None:
        """
        Test that get_token calls refresh_token when is_new=True, even if a valid token exists.
        """
        provider = self.DummyTokenProvider()
        provider._token = "cached-token"
        provider.next_token = "fresh-token"

        token = await provider.get_token(is_new=True)

        assert provider.refresh_calls == 1
        assert token == "fresh-token"

    async def test_get_token_refreshes_when_expired(self) -> None:
        """Test that get_token calls refresh_token when the token is expired."""
        provider = self.DummyTokenProvider()
        provider._token = "expired-token"
        provider._token_expiry = datetime.now() - timedelta(seconds=1)
        provider.next_token = "renewed-token"

        token = await provider.get_token()

        assert provider.refresh_calls == 1
        assert token == "renewed-token"

    async def test_auth_header_returns_bearer_token(self) -> None:
        """Test that auth_header returns the correct Bearer token."""
        provider = self.DummyTokenProvider()
        provider._token = "test-token"

        header = await provider.auth_header()

        assert header == {"Authorization": "Bearer test-token"}

    async def test_auth_header_returns_empty_when_no_token(self) -> None:
        """Test that auth_header returns an empty dictionary when no token is available."""
        provider = self.DummyTokenProvider()
        provider.next_token = None

        header = await provider.auth_header()

        assert header == {}

    async def test_refresh_token_raises_not_implemented(self) -> None:
        """Test that the base refresh_token method raises NotImplementedError."""
        provider = BaseTokenProvider(service="test-service", type_="Base")

        with pytest.raises(NotImplementedError):
            await provider.refresh_token()

    async def test_close_calls_checkpoint(self) -> None:
        """Test that close calls the anyio checkpoint."""
        provider = self.DummyTokenProvider()

        with patch(
            "apaleoapi.http.auth.anyio.lowlevel.checkpoint",
            new_callable=AsyncMock,
        ) as checkpoint:
            await provider.aclose()

        checkpoint.assert_awaited_once()


class TestOAuth2ClientCredentialsProvider:
    """
    Tests for the OAuth2ClientCredentialsProvider class,
    which implements the client credentials flow.
    """

    async def test_refresh_token_success_with_optional_fields(self) -> None:
        """
        Test that refresh_token successfully retrieves and stores the access token,
        including optional fields.
        """
        provider = OAuth2ClientCredentialsProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            token_url="https://identity.example.com/token",
            scope="scope.read",
            audience="api.audience",
            extra={"custom": "value"},
            timeout=15,
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {"access_token": "access-token"}

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            await provider.refresh_token()

        assert provider._token == "access-token"
        async_client_cls.assert_called_once_with(timeout=15, verify=True)
        async_client.post.assert_awaited_once_with(
            "https://identity.example.com/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "client-id",
                "client_secret": "client-secret",
                "custom": "value",
                "scope": "scope.read",
                "audience": "api.audience",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    async def test_refresh_token_raises_for_non_200(self) -> None:
        """Test that refresh_token raises a RuntimeError when the response status is not 200."""
        provider = OAuth2ClientCredentialsProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 401

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            with pytest.raises(RuntimeError, match="Authentication failed"):
                await provider.refresh_token()

    async def test_refresh_token_raises_when_access_token_missing(self) -> None:
        """Test that refresh_token raises a RuntimeError when the access token is missing."""
        provider = OAuth2ClientCredentialsProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {}

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            with pytest.raises(RuntimeError, match="no access_token"):
                await provider.refresh_token()


class TestOAuth2AuthorizationCodeProvider:
    """
    Tests for the OAuth2AuthorizationCodeProvider class,
    which implements the authorization code flow.
    """

    async def test_refresh_token_exchanges_authorization_code(self) -> None:
        """
        Test that refresh_token successfully exchanges the authorization code for an access token.
        """
        provider = OAuth2AuthorizationCodeProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            redirect_uri="https://app.example.com/callback",
            token_url="https://identity.example.com/token",
            extra={"authorization_code": "auth-code"},
            timeout=20,
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {
            "access_token": "initial-token",
            "refresh_token": "refresh-token-1",
            "expires_in": 120,
        }

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            await provider.refresh_token()

        assert provider._token == "initial-token"
        assert provider._refresh_token == "refresh-token-1"
        assert provider._token_expiry is not None
        async_client_cls.assert_called_once_with(timeout=20, verify=True)
        async_client.post.assert_awaited_once_with(
            "https://identity.example.com/token",
            data={
                "grant_type": "authorization_code",
                "code": "auth-code",
                "redirect_uri": "https://app.example.com/callback",
                "client_id": "client-id",
                "client_secret": "client-secret",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    async def test_refresh_token_uses_refresh_token_after_initial_exchange(self) -> None:
        """Test that refresh_token uses the refresh token after the initial exchange."""
        provider = OAuth2AuthorizationCodeProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            redirect_uri="https://app.example.com/callback",
            token_url="https://identity.example.com/token",
            timeout=20,
        )
        provider._token = "existing-token"
        provider._refresh_token = "existing-refresh-token"

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {
            "access_token": "renewed-token",
            "refresh_token": "refresh-token-2",
        }

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            await provider.refresh_token()

        assert provider._token == "renewed-token"
        assert provider._refresh_token == "refresh-token-2"
        async_client.post.assert_awaited_once_with(
            "https://identity.example.com/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": "existing-refresh-token",
                "client_id": "client-id",
                "client_secret": "client-secret",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    async def test_refresh_token_keeps_existing_refresh_token_when_missing(self) -> None:
        """
        Test that refresh_token keeps the existing refresh token
        if the response does not include a new one.
        """
        provider = OAuth2AuthorizationCodeProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            redirect_uri="https://app.example.com/callback",
            token_url="https://identity.example.com/token",
        )
        provider._token = "existing-token"
        provider._refresh_token = "existing-refresh-token"

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {"access_token": "renewed-token"}

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            await provider.refresh_token()

        assert provider._token == "renewed-token"
        assert provider._refresh_token == "existing-refresh-token"

    async def test_refresh_token_raises_for_non_200(self) -> None:
        """Test that refresh_token raises a RuntimeError when the response status is not 200."""
        provider = OAuth2AuthorizationCodeProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            redirect_uri="https://app.example.com/callback",
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 400

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            with pytest.raises(RuntimeError, match="Authentication failed"):
                await provider.refresh_token()

    async def test_refresh_token_raises_when_access_token_missing(self) -> None:
        """Test that refresh_token raises a RuntimeError when the access token is missing."""
        provider = OAuth2AuthorizationCodeProvider(
            client_id="client-id",
            client_secret="client-secret",
            service="test-service",
            redirect_uri="https://app.example.com/callback",
        )

        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {"refresh_token": "new-refresh-token"}

        async_client = AsyncMock()
        async_client.post.return_value = response

        with patch("apaleoapi.http.auth.httpx.AsyncClient") as async_client_cls:
            async_client_cls.return_value.__aenter__.return_value = async_client

            with pytest.raises(RuntimeError, match="no access_token"):
                await provider.refresh_token()
