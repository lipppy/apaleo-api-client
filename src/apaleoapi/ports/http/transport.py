from typing import Any, Mapping, Optional, Protocol

import httpx


class AsyncTransportPort(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        *,
        content: Optional[bytes] = None,
        data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[dict[str, Any]] = None,
        json: Any = None,
    ) -> httpx.Response:
        """Make an HTTP request."""
        pass

    async def aclose(self) -> None:
        """Close the transport."""
        pass
