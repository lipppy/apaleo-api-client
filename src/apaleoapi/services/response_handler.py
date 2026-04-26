from typing import Any, cast

import httpx

from apaleoapi.exceptions import (
    APIError,
    BadRequestError,
    ClientClosedRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ServiceUnavailableError,
    UnauthorizedError,
    ValidationError,
)
from apaleoapi.logging import get_logger

log = get_logger(__name__)


class ResponseHandler:
    """
    Handles API responses, raising exceptions for error statuses
    and returning parsed data for successful responses.
     - For 200 responses, it returns the parsed JSON or text.
     - For 204 responses, it returns None.
     - For 400, 401, 403, 404, 422, 499, 500, 503 responses,
       it raises appropriate exceptions with messages.
     - For any other unexpected status, it raises a generic APIError.
     - For 422 responses, it attempts to extract validation error messages
       from the response body and includes them in the exception message.
    """

    def __init__(self) -> None:
        """Initialize the response handler."""
        pass

    def handle(self, response: httpx.Response) -> str | dict[str, Any] | list[Any] | None:
        """
        Main entry point.
        Returns parsed success response or raises appropriate exception.
        """
        status = response.status_code

        match status:
            case 200 | 201 | 202 | 203:
                return self._handle_success(response)
            case 204:
                return None
            case 400:
                raise BadRequestError("Bad request.", response)
            case 401:
                raise UnauthorizedError("You are unauthorized.", response)
            case 403:
                raise ForbiddenError("Forbidden.", response)
            case 404:
                raise NotFoundError("The Request-URI could not be found.", response)
            case 422:
                raise self._handle_validation_error(response)
            case 499:
                raise ClientClosedRequestError("Client closed request.", response)
            case 500:
                raise InternalServerError("An unexpected error occurred.", response)
            case 503:
                raise ServiceUnavailableError(
                    "The server is currently unavailable. Please try later.",
                    response,
                )

        # Fallback for any unhandled status
        raise APIError(
            f"Unexpected status code: {status}",
            response,
        )

    def _handle_success(self, response: httpx.Response) -> str | dict[str, Any] | list[Any]:
        """
        Default success handler.
        Override in subclasses if you need model parsing.
        """
        if response.headers.get("content-type", "").startswith("application/json"):
            return cast(dict[str, Any] | list[Any], response.json())
        return response.text

    def _handle_validation_error(self, response: httpx.Response) -> ValidationError:
        """
        Extracts validation messages from 422 response.
        Expected format:
        {
            "messages": ["string"]
        }
        """
        try:
            data = cast(dict[str, Any], response.json())
            messages = data.get("messages", [])
        except Exception:
            messages = ["Unable to parse validation error messages."]

        message = "Validation errors in the request body or query params."
        if messages:
            message += f" Details: {', '.join(messages)}"

        return ValidationError(message, response, errors=messages)
