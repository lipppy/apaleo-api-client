# Identity API


from apaleoapi.apaleo.identity.v1.apis.identity import IdentityV1IdentityResource
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.client import APIPort, VersionPort


class IdentityAPI(APIPort):
    """Top-level entry point for the entire Identity API domain"""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.v1 = IdentityV1Version(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )
        self.nsfw = IdentityNSFWVersion(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class IdentityV1Version(VersionPort):
    """Version-specific coordinator for v1 endpoints"""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        self.identity = IdentityV1IdentityResource(
            transport=transport, max_concurrent=max_concurrent, dry_run=dry_run
        )


class IdentityNSFWVersion(VersionPort):
    """Version-specific coordinator for nsfw endpoints."""

    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass
