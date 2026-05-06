from typing import Protocol


class URLPathValidatorPort(Protocol):
    def validate(self, value: str) -> str:
        """Validate and normalize an API path, ensuring it is safe and well-formed."""
        pass
