from typing import Any
from unittest.mock import Mock

import httpx
import pytest

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
from apaleoapi.services.response_handler import ResponseHandler

pytestmark = [pytest.mark.unit]


class TestResponseHandler:
    """Test cases for ResponseHandler."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.handler = ResponseHandler()

    @staticmethod
    def _create_mock_response(
        status_code: int,
        content_type: str,
        data: Any,
    ) -> Mock:
        """Create a mock httpx.Response for testing."""
        response = Mock(spec=httpx.Response)
        response.status_code = status_code
        response.headers = {"content-type": content_type}
        response.text = str(data) if not isinstance(data, str) else data
        response.json.return_value = data
        return response

    @pytest.mark.parametrize(
        "status_code,content_type,response_data,expected",
        [
            # 200 OK with JSON
            (200, "application/json", {"id": 1, "name": "test"}, {"id": 1, "name": "test"}),
            # 200 OK with JSON list
            (200, "application/json", [{"id": 1}, {"id": 2}], [{"id": 1}, {"id": 2}]),
            # 200 OK with text
            (200, "text/plain", "success", "success"),
            # 201 Created with JSON
            (201, "application/json", {"id": 1}, {"id": 1}),
            # 201 Created with text
            (201, "text/plain", "created", "created"),
            # 202 Accepted with JSON
            (202, "application/json", {"status": "accepted"}, {"status": "accepted"}),
            # 202 Accepted with text
            (202, "text/plain", "accepted", "accepted"),
            # 203 Non-Authoritative Information with JSON
            (203, "application/json", {"info": "non-authoritative"}, {"info": "non-authoritative"}),
            # 203 Non-Authoritative Information with text
            (203, "text/plain", "non-authoritative", "non-authoritative"),
            # 204 No Content
            (204, "text/plain", "", None),
            (204, "application/json", None, None),
        ],
    )
    def test_handle_success_responses(
        self, status_code: int, content_type: str, response_data: Any, expected: Any
    ) -> None:
        """Test handling of successful responses (200, 201, 202, 203, 204)."""
        response = self._create_mock_response(status_code, content_type, response_data)
        result = self.handler.handle(response)
        assert result == expected

    @pytest.mark.parametrize(
        "status_code,exception_class,expected_message",
        [
            (400, BadRequestError, "Bad request."),
            (401, UnauthorizedError, "You are unauthorized."),
            (403, ForbiddenError, "Forbidden."),
            (404, NotFoundError, "The Request-URI could not be found."),
            (499, ClientClosedRequestError, "Client closed request."),
            (500, InternalServerError, "An unexpected error occurred."),
            (
                503,
                ServiceUnavailableError,
                "The server is currently unavailable. Please try later.",
            ),
        ],
    )
    def test_handle_error_responses(
        self, status_code: int, exception_class: type[APIError], expected_message: str
    ) -> None:
        """Test handling of error responses."""
        response = self._create_mock_response(status_code, "application/json", {})
        with pytest.raises(exception_class) as exc_info:
            self.handler.handle(response)
        assert str(exc_info.value) == expected_message
        assert exc_info.value.status_code == status_code
        assert exc_info.value.response == response

    def test_handle_validation_error_with_messages(self) -> None:
        """Test handling of 422 Validation Error with messages."""
        response = self._create_mock_response(
            422,
            "application/json",
            {"messages": ["Invalid email format", "Name is required"]},
        )
        with pytest.raises(ValidationError) as exc_info:
            self.handler.handle(response)
        exc = exc_info.value
        assert "Validation errors in the request body or query params." in str(exc)
        assert "Invalid email format" in str(exc)
        assert "Name is required" in str(exc)
        assert exc.errors == ["Invalid email format", "Name is required"]
        assert exc.status_code == 422

    def test_handle_validation_error_empty_messages(self) -> None:
        """Test handling of 422 Validation Error with empty messages."""
        response = self._create_mock_response(422, "application/json", {"messages": []})
        with pytest.raises(ValidationError) as exc_info:
            self.handler.handle(response)
        exc = exc_info.value
        assert "Validation errors in the request body or query params." in str(exc)
        assert exc.errors == []

    def test_handle_validation_error_invalid_json(self) -> None:
        """Test handling of 422 with invalid JSON response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 422
        response.json.side_effect = ValueError("Invalid JSON")
        with pytest.raises(ValidationError) as exc_info:
            self.handler.handle(response)
        exc = exc_info.value
        assert "Unable to parse validation error messages." in str(exc)
        assert exc.errors == ["Unable to parse validation error messages."]

    def test_handle_validation_error_missing_messages_key(self) -> None:
        """Test handling of 422 with missing messages key."""
        response = self._create_mock_response(422, "application/json", {"error": "something"})
        with pytest.raises(ValidationError) as exc_info:
            self.handler.handle(response)
        exc = exc_info.value
        assert "Validation errors in the request body or query params." in str(exc)
        assert exc.errors == []

    def test_handle_unexpected_status_code(self) -> None:
        """Test handling of unexpected status codes."""
        response = self._create_mock_response(418, "application/json", {})
        with pytest.raises(APIError) as exc_info:
            self.handler.handle(response)
        assert "Unexpected status code: 418" in str(exc_info.value)
        assert exc_info.value.status_code == 418

    def test_handle_success_with_charset(self) -> None:
        """Test successful response with content-type including charset."""
        response = self._create_mock_response(
            200, "application/json; charset=utf-8", {"key": "value"}
        )
        result = self.handler.handle(response)
        assert result == {"key": "value"}

    def test_handle_success_with_non_json_text(self) -> None:
        """Test successful response with non-JSON text content."""
        response = self._create_mock_response(200, "text/html", "<html>content</html>")
        result = self.handler.handle(response)
        assert result == "<html>content</html>"

    def test_handle_success_response_without_content_type(self) -> None:
        """Test successful response without content-type header."""
        response = self._create_mock_response(200, "", "plain text")
        result = self.handler.handle(response)
        assert result == "plain text"
