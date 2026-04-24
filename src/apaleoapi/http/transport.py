from typing import Any, Mapping, Optional

import httpx
from httpx_retries import Retry, RetryTransport

from apaleoapi.logging import get_logger
from apaleoapi.ports.http.auth import TokenProviderPort
from apaleoapi.ports.http.transport import AsyncTransportPort

log = get_logger(__name__)


class AuthenticatedTransport(AsyncTransportPort):
    """HTTP transport with automatic token authentication and refresh."""

    _header_content_type: str

    def __init__(
        self,
        base_url: str,
        token_provider: TokenProviderPort,
        timeout: float = 10.0,
        retries: int = 1,
        header_content_type: str = "application/json",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token_provider = token_provider
        retry = Retry(total=retries, backoff_factor=0.5)
        transport = RetryTransport(retry=retry)
        self.client = httpx.AsyncClient(timeout=timeout, transport=transport, verify=True)
        self._header_content_type = header_content_type

    async def request(
        self,
        method: str,
        path: str,
        *,
        content: Optional[bytes] = None,
        data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[dict[str, Any]] = None,
        json: Any = None,
    ) -> httpx.Response:
        """Make an authenticated HTTP request, refreshing the token if necessary."""
        token_header = await self.token_provider.auth_header()
        headers = {
            **token_header,
            "Content-Type": self._header_content_type,
            **(headers or {}),
        }
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.request(
            method, url, content=content, data=data, headers=headers, params=params, json=json
        )

        # If unauthorized, refresh the token and retry once
        if response.status_code == 401:
            log.info("Token expired or invalid. Refreshing token...")
            token_header = await self.token_provider.auth_header(is_new=True)
            headers.update(token_header)
            response = await self.client.request(
                method, url, content=content, data=data, headers=headers, params=params, json=json
            )

        return response

    async def aclose(self) -> None:
        """Close the HTTP client session."""
        await self.client.aclose()
