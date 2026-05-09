from unittest.mock import AsyncMock, Mock, patch

import pytest

from apaleoapi.apaleo.core.api import CoreAPI, CoreNSFWVersion, CoreV1Version
from apaleoapi.apaleo.identity.api import IdentityAPI, IdentityV1Version
from apaleoapi.client import ApaleoAPIClient

pytestmark = [pytest.mark.unit]


class TestApaleoAPIClient:
    """Test cases for ApaleoAPIClient."""

    def test_client_initialization_minimal(self, mock_token_provider: Mock) -> None:
        """Test minimal client initialization."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider)
            assert client.token_provider == mock_token_provider
            assert client._timeout == 10.0  # Default value
            assert client._retries == 1  # Default value
            assert client._max_concurrent == 2  # Default value
            assert client._dry_run is False  # Default value

    def test_client_initialization_with_all_options(self, mock_token_provider: Mock) -> None:
        """Test client initialization with all options specified."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(
                token_provider=mock_token_provider,
                timeout=20.0,
                retries=3,
                max_concurrent=10,
                dry_run=True,
            )
            assert client.token_provider == mock_token_provider
            assert client._timeout == 20.0
            assert client._retries == 3
            assert client._max_concurrent == 10
            assert client._dry_run is True

    def test_client_initialization_with_dry_run(self, mock_token_provider: Mock) -> None:
        """Test client initialization with dry run enabled."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider, dry_run=True)
            assert client.token_provider == mock_token_provider
            assert client._dry_run is True

    def test_client_repr(self, mock_token_provider: Mock) -> None:
        """Test client string representation."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider)
            repr_str = repr(client)
            assert "ApaleoAPIClient" in repr_str
            assert "dry_run=False" in repr_str

    def test_client_repr_dry_run_true(self, mock_token_provider: Mock) -> None:
        """Test client string representation with dry run enabled."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider, dry_run=True)
            repr_str = repr(client)
            assert "dry_run=True" in repr_str

    @pytest.mark.asyncio
    async def test_client_aclose(self, mock_token_provider: Mock) -> None:
        """Test client cleanup method."""
        with patch("apaleoapi.client.AuthenticatedTransport") as mock_transport_class:
            # Set up mock transport instances
            mock_transport = AsyncMock()
            mock_transport.aclose = AsyncMock()
            mock_transport_class.return_value = mock_transport

            client = ApaleoAPIClient(token_provider=mock_token_provider)
            await client.aclose()

            # Verify all transports were closed (7 different API endpoints)
            assert mock_transport.aclose.call_count == 7

    def test_client_has_core_adapter(self, mock_token_provider: Mock) -> None:
        """Test that client has core adapter properly initialized."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider)
            assert hasattr(client, "core")
            assert isinstance(client.core, CoreAPI)

    def test_client_has_identity_adapter(self, mock_token_provider: Mock) -> None:
        """Test that client has identity adapter properly initialized."""
        with patch("apaleoapi.client.AuthenticatedTransport"):
            client = ApaleoAPIClient(token_provider=mock_token_provider)
            assert hasattr(client, "identity")
            assert isinstance(client.identity, IdentityAPI)

    def test_core_api_initialization(
        self,
        mock_transport: Mock,
        mock_response_handler: Mock,
        mock_response_validator: Mock,
        mock_url_path_validator: Mock,
    ) -> None:
        """Test Core API initialization."""
        adapter = CoreAPI(
            transport=mock_transport,
            response_handler=mock_response_handler,
            response_validator=mock_response_validator,
            url_path_validator=mock_url_path_validator,
            max_concurrent=5,
            dry_run=False,
        )

        assert hasattr(adapter, "v1")
        assert hasattr(adapter, "nsfw")
        assert isinstance(adapter.v1, CoreV1Version)
        assert isinstance(adapter.nsfw, CoreNSFWVersion)

    def test_core_v1_version_initialization(
        self,
        mock_transport: Mock,
        mock_response_handler: Mock,
        mock_response_validator: Mock,
        mock_url_path_validator: Mock,
    ) -> None:
        """Test Core API V1 version initialization."""
        adapter = CoreV1Version(
            transport=mock_transport,
            response_handler=mock_response_handler,
            response_validator=mock_response_validator,
            url_path_validator=mock_url_path_validator,
            max_concurrent=5,
            dry_run=False,
        )

        assert hasattr(adapter, "inventory")

    def test_identity_api_initialization(
        self,
        mock_transport: Mock,
        mock_response_handler: Mock,
        mock_response_validator: Mock,
        mock_url_path_validator: Mock,
    ) -> None:
        """Test Identity API initialization."""
        adapter = IdentityAPI(
            transport=mock_transport,
            response_handler=mock_response_handler,
            response_validator=mock_response_validator,
            url_path_validator=mock_url_path_validator,
            max_concurrent=5,
            dry_run=False,
        )

        assert hasattr(adapter, "v1")
        assert isinstance(adapter.v1, IdentityV1Version)

    def test_identity_v1_version_initialization(
        self,
        mock_transport: Mock,
        mock_response_handler: Mock,
        mock_response_validator: Mock,
        mock_url_path_validator: Mock,
    ) -> None:
        """Test Identity API V1 version initialization."""
        adapter = IdentityV1Version(
            transport=mock_transport,
            response_handler=mock_response_handler,
            response_validator=mock_response_validator,
            url_path_validator=mock_url_path_validator,
            max_concurrent=5,
            dry_run=False,
        )

        assert hasattr(adapter, "identity")

    def test_client_transports_initialization(
        self, mock_token_provider: Mock, mock_transport: Mock
    ) -> None:
        """Test that all transport instances are properly initialized."""
        with patch("apaleoapi.client.AuthenticatedTransport") as mock_transport_class:
            mock_transport_class.return_value = mock_transport

            _ = ApaleoAPIClient(token_provider=mock_token_provider)

            # Verify that AuthenticatedTransport was called for each API
            assert mock_transport_class.call_count == 7  # 7 different API endpoints
