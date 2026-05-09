from posixpath import normpath
from urllib.parse import unquote, urlparse

from apaleoapi.ports.validation.url_path_validator import URLPathValidatorPort


class URLPathValidationError(ValueError):
    """Raised when an API path is invalid or unsafe."""


class URLPathValidator(URLPathValidatorPort):
    def validate(self, value: str) -> str:
        """Validate and normalize an API path, ensuring it is safe and well-formed."""
        if not isinstance(value, str):
            raise URLPathValidationError("Path must be a string")

        # Decode URL-encoded characters and normalize the path to prevent path traversal
        raw_path = unquote(urlparse(value).path)

        # Check for path traversal patterns (e.g., "..") in the raw path
        if ".." in raw_path.split("/"):
            raise URLPathValidationError("Path traversal detected")

        # Normalize the path to remove redundant separators and up-level references
        path = normpath(raw_path)

        # Ensure the normalized path is absolute and does not contain unsafe segments
        if path == ".":
            return "/"

        # Ensure the path starts with a slash for consistency
        return path if path.startswith("/") else f"/{path}"
