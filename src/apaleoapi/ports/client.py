from typing import Protocol

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
