"""Test configuration for pytest."""

from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from apaleoapi.client import ApaleoAPIClient
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider
from apaleoapi.http.response_handler import ResponseHandler
from apaleoapi.http.response_validator import ResponseValidator
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.http.response_handler import ResponseHandlerPort
from apaleoapi.ports.http.response_validator import ResponseValidatorPort
from apaleoapi.ports.validation.url_path_validator import URLPathValidatorPort
from apaleoapi.validation.url_path_validator import URLPathValidator


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
    transport = AsyncMock(spec=AuthenticatedTransport)
    transport.request = AsyncMock()
    transport.aclose = AsyncMock()
    return transport


@pytest.fixture
def mock_token_provider() -> Mock:
    """Mock token provider for testing."""
    token_provider = Mock(spec=OAuth2ClientCredentialsProvider)
    token_provider.get_token = AsyncMock(return_value="mock-token")
    token_provider.auth_header = AsyncMock(return_value={"Authorization": "Bearer mock-token"})
    token_provider.close = AsyncMock()
    return token_provider


@pytest.fixture
def mock_response_handler() -> Mock:
    """Mock response handler for testing."""
    handler = Mock(spec=ResponseHandlerPort)
    return handler


@pytest.fixture
def response_handler() -> ResponseHandlerPort:
    """Real response handler for testing."""
    handler = ResponseHandler()
    return handler


@pytest.fixture
def mock_response_validator() -> Mock:
    """Mock response validator for testing."""
    validator = Mock(spec=ResponseValidatorPort)
    return validator


@pytest.fixture
def response_validator() -> ResponseValidatorPort:
    """Real response validator for testing."""
    validator = ResponseValidator()
    return validator


@pytest.fixture
def mock_url_path_validator() -> Mock:
    """Mock URL path validator for testing."""
    validator = Mock(spec=URLPathValidatorPort)
    validator.validate = Mock(side_effect=lambda url: f"validated/{url}")
    return validator


@pytest.fixture
def url_path_validator() -> URLPathValidatorPort:
    """Real URL path validator for testing."""
    validator = URLPathValidator()
    return validator


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
