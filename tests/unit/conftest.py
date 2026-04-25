"""Test configuration for pytest."""

from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from apaleoapi.client import ApaleoAPIClient
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider


@pytest.fixture
def sample_client_id() -> str:
    """Sample client ID for testing."""
    return "test-client-id-123"


@pytest.fixture
def sample_client_secret() -> str:
    """Sample client secret for testing."""
    return "test-client-secret-456"


@pytest.fixture
def sample_base_url() -> str:
    """Sample base URL for testing."""
    return "https://test.api.apaleo.invalid.com"


@pytest.fixture
def mock_transport() -> AsyncMock:
    """Mock transport for testing."""
    transport = AsyncMock()
    transport.aclose = AsyncMock()
    return transport


@pytest.fixture
def mock_token_provider() -> Mock:
    """Mock token provider for testing."""
    token_provider = Mock()
    token_provider.get_token = AsyncMock(return_value="mock-token")
    token_provider.auth_header = AsyncMock(return_value={"Authorization": "Bearer mock-token"})
    token_provider.close = AsyncMock()
    return token_provider


@pytest.fixture
def mock_client_config(mock_token_provider: Mock) -> dict[str, Any]:
    """Configuration for mock client."""
    return {
        "token_provider": mock_token_provider,
        "timeout": 15.0,
        "retries": 2,
        "max_concurrent": 5,
        "dry_run": False,
    }


@pytest.fixture
async def mock_client(mock_client_config: dict[str, Any]) -> AsyncGenerator[ApaleoAPIClient, None]:
    """Create a mocked Apaleo API client for testing."""
    with patch("apaleoapi.client.AuthenticatedTransport") as mock_transport_class:
        # Set up mock transport instances
        mock_transport = AsyncMock()
        mock_transport.aclose = AsyncMock()
        mock_transport_class.return_value = mock_transport

        client = ApaleoAPIClient(**mock_client_config)
        yield client
        await client.aclose()


@pytest.fixture
def client_credentials(sample_client_id: str, sample_client_secret: str) -> dict[str, str]:
    """Basic client credentials fixture."""
    return {"client_id": sample_client_id, "client_secret": sample_client_secret}


@pytest.fixture
def oauth2_token_provider(
    sample_client_id: str, sample_client_secret: str
) -> OAuth2ClientCredentialsProvider:
    """OAuth2 client credentials token provider fixture."""
    return OAuth2ClientCredentialsProvider(
        token_url="https://identity.test.apaleo.com/connect/token",
        client_id=sample_client_id,
        client_secret=sample_client_secret,
        service="test-service",
    )
