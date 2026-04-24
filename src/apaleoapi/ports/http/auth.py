from datetime import datetime
from typing import Protocol


class TokenProviderPort(Protocol):
    """Protocol for token providers used in authenticated HTTP requests."""

    _service: str
    _type: str
    _token: str | None
    _token_expiry: datetime | None

    async def get_token(self, is_new: bool = False) -> str | None:
        """Get the current access token, refreshing it if necessary."""
        pass

    async def refresh_token(self) -> None:
        """Refresh the access token."""
        pass

    async def auth_header(self, is_new: bool = False) -> dict[str, str]:
        """Get the authorization header value."""
        pass

    async def close(self) -> None:
        """Close any resources held by the token provider."""
        pass
