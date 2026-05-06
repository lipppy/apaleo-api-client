from typing import Any, Protocol

import httpx


class ResponseHandlerPort(Protocol):
    def handle(self, response: httpx.Response) -> str | dict[str, Any] | list[Any] | None:
        """Returns parsed success response or raises appropriate exception."""
        pass
