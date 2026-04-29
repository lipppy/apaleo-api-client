from typing import Protocol

from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.http.auth import TokenProviderPort


class ApaleoAPIClientPort(Protocol):
    def __init__(
        self,
        token_provider: TokenProviderPort,
        timeout: float,
        retries: int,
        max_concurrent: int,
        dry_run: bool,
    ):
        pass

    async def aclose(self) -> None:
        pass


class APIPort(Protocol):
    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass


class VersionPort(Protocol):
    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass


class ResourcePort(Protocol):
    def __init__(
        self, transport: AuthenticatedTransport, max_concurrent: int, dry_run: bool
    ) -> None:
        pass
