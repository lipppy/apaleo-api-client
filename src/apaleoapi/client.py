"""Apaleo API Client implementation."""

from apaleoapi.apaleo.core.v1.apis.inventory import CoreV1InventoryAdapter
from apaleoapi.apaleo.identity.v1.apis.identity import IdentityV1IdentityResource
from apaleoapi.constants import (
    APALEO_API_CORE_URL,
    APALEO_API_FISCALIZATION_URL,
    APALEO_API_IDENTITY_URL,
    APALEO_API_INTEGRATION_URL,
    APALEO_API_PAYMENT_URL,
    APALEO_API_PROFILE_URL,
    APALEO_API_WEBHOOK_URL,
)
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.client import ApaleoAPIClientPort
from apaleoapi.ports.http.auth import TokenProviderPort


class ApaleoAPIClient(ApaleoAPIClientPort):
    """Main client for interacting with Apaleo API."""

    def __init__(
        self,
        token_provider: TokenProviderPort,
        timeout: float = 10.0,
        retries: int = 1,
        max_concurrent: int = 2,
        dry_run: bool = False,
    ) -> None:
        """Initialize Apaleo API client.

        Args:
            token_provider: Token provider for OAuth2 authentication
            timeout: Request timeout in seconds (default: 10)
            retries: Number of retries for API requests (default: 1)
            max_concurrent: Maximum number of concurrent API requests (default: 10)
            dry_run: If True, do not make actual API calls (default: False)
        """
        self.__token_provider = token_provider
        self._timeout = timeout
        self._retries = retries
        self._max_concurrent = max_concurrent
        self._dry_run = dry_run

        # Initialize transports for different Apaleo API domains
        transport_identity_api = AuthenticatedTransport(
            base_url=APALEO_API_IDENTITY_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_core_api = AuthenticatedTransport(
            base_url=APALEO_API_CORE_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_webhook_api = AuthenticatedTransport(
            base_url=APALEO_API_WEBHOOK_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_integration_api = AuthenticatedTransport(
            base_url=APALEO_API_INTEGRATION_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_fiscalization_api = AuthenticatedTransport(
            base_url=APALEO_API_FISCALIZATION_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_payment_api = AuthenticatedTransport(
            base_url=APALEO_API_PAYMENT_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )
        transport_profile_api = AuthenticatedTransport(
            base_url=APALEO_API_PROFILE_URL,
            token_provider=self.__token_provider,
            timeout=self._timeout,
            retries=self._retries,
        )

        # Store transports as instance variables
        self.__transport_core_api = transport_core_api
        self.__transport_fiscalization_api = transport_fiscalization_api
        self.__transport_identity_api = transport_identity_api
        self.__transport_integration_api = transport_integration_api
        self.__transport_payment_api = transport_payment_api
        self.__transport_profile_api = transport_profile_api
        self.__transport_webhook_api = transport_webhook_api

        # Core API adapters
        self.core = CoreAPI(
            transport=transport_core_api, max_concurrent=self._max_concurrent, dry_run=self._dry_run
        )
        # Fiscalization API adapters
        # Identity API adapters
        self.identity = IdentityAPI(
            transport=transport_identity_api,
            max_concurrent=self._max_concurrent,
            dry_run=self._dry_run,
        )
        # Integration API adapters
        # Payment API adapters
        # Profile API adapters
        # Webhook API adapters

    @property
    def token_provider(self) -> TokenProviderPort:
        """Return the token provider used by the client."""
        return self.__token_provider

    def __repr__(self) -> str:
        """Return string representation of client."""
        return (
            "ApaleoAPIClient("
            f"token_provider={self.token_provider.__class__.__name__}, "
            f"timeout={self._timeout}, "
            f"retries={self._retries}, "
            f"max_concurrent={self._max_concurrent}, "
            f"dry_run={self._dry_run})"
        )

    async def aclose(self) -> None:
        """Close all transports and clean up resources."""
        await self.__transport_core_api.aclose()
        await self.__transport_fiscalization_api.aclose()
        await self.__transport_identity_api.aclose()
        await self.__transport_integration_api.aclose()
        await self.__transport_payment_api.aclose()
        await self.__transport_profile_api.aclose()
        await self.__transport_webhook_api.aclose()


# Core API adapters


class CoreAPI:
    """Adapter for Core API endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.v1 = CoreV1Version(transport=transport, max_concurrent=max_concurrent, dry_run=dry_run)
        self.nsfw = CoreNSFWVersion(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class CoreV1Version:
    """Adapter for Core V1 API endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.inventory = CoreV1InventoryAdapter(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class CoreNSFWVersion:
    """Adapter for Core NSFW API endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass


# Identity API adapters


class IdentityAPI:
    """Adapter for Identity API endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.v1 = IdentityV1Version(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class IdentityV1Version:
    """Adapter for Identity V1 API endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.identity = IdentityV1IdentityResource(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )
