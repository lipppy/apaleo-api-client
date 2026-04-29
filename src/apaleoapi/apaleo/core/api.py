# Core API


from apaleoapi.apaleo.core.v1.apis.inventory import CoreV1InventoryResource
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.client import APIPort, VersionPort


class CoreAPI(APIPort):
    """Top-level entry point for the entire Core API domain"""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.v1 = CoreV1Version(transport=transport, max_concurrent=max_concurrent, dry_run=dry_run)
        self.nsfw = CoreNSFWVersion(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class CoreV1Version(VersionPort):
    """Version-specific coordinator for v1 endpoints"""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.inventory = CoreV1InventoryResource(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class CoreNSFWVersion(VersionPort):
    """Version-specific coordinator for nsfw endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass
