from typing import Any, List
from unittest.mock import Mock

import httpx
import pytest
from pydantic import BaseModel, RootModel
from pydantic import ValidationError as PydanticValidationError

from apaleoapi.exceptions import ValidationError
from apaleoapi.http.response_validator import ResponseValidator

pytestmark = [pytest.mark.unit]


class SampleModel(BaseModel):
    """Sample Pydantic model for validation testing."""

    id: int
    name: str
    optional_field: str | None = None


class TestResponseValidator:
    """Test cases for ResponseValidator."""

    @staticmethod
    def _create_mock_response(status_code: int = 200) -> Mock:
        """Create a mock httpx.Response for testing."""
        response = Mock(spec=httpx.Response)
        response.status_code = status_code
        return response

    def test_validate_success_with_dict(self) -> None:
        """Test successful validation with dictionary data."""
        response_data = {"id": 123, "name": "Test Item"}
        response = self._create_mock_response()
        error_prefix = "Failed to parse response"

        result = ResponseValidator.validate(
            response_data=response_data,
            response=response,
            model_cls=SampleModel,
            error_prefix=error_prefix,
        )

        assert isinstance(result, SampleModel)
        assert result.id == 123
        assert result.name == "Test Item"
        assert result.optional_field is None

    def test_validate_success_with_optional_field(self) -> None:
        """Test successful validation with optional field included."""
        response_data = {"id": 456, "name": "Test Item", "optional_field": "optional"}
        response = self._create_mock_response()
        error_prefix = "Failed to parse response"

        result = ResponseValidator.validate(
            response_data=response_data,
            response=response,
            model_cls=SampleModel,
            error_prefix=error_prefix,
        )

        assert isinstance(result, SampleModel)
        assert result.id == 456
        assert result.name == "Test Item"
        assert result.optional_field == "optional"

    def test_validate_success_with_list_data(self) -> None:
        """Test successful validation with list data for model that accepts lists."""

        class ModelList(RootModel[List[SampleModel]]):
            pass

        response_data = [{"id": 1, "name": "First"}, {"id": 2, "name": "Second"}]
        response = self._create_mock_response()
        error_prefix = "Failed to parse list response"

        result = ResponseValidator.validate(
            response_data=response_data,
            response=response,
            model_cls=ModelList,
            error_prefix=error_prefix,
        )

        assert isinstance(result, ModelList)
        assert len(result.root) == 2
        assert result.root[0].name == "First"
        assert result.root[1].name == "Second"

    def test_validate_pydantic_validation_error(self) -> None:
        """Test ValidationError is raised when Pydantic validation fails."""
        response_data = {"id": "not-an-int", "name": "Test Item"}  # id should be int
        response = self._create_mock_response()
        error_prefix = "Failed to parse API response"

        with pytest.raises(ValidationError) as exc_info:
            ResponseValidator.validate(
                response_data=response_data,
                response=response,
                model_cls=SampleModel,
                error_prefix=error_prefix,
            )

        # Verify the ValidationError contains the prefix
        assert "Failed to parse API response:" in str(exc_info.value)
        # Verify the original response is attached
        assert exc_info.value.response == response
        # Verify the exception chain
        assert isinstance(exc_info.value.__cause__, PydanticValidationError)

    def test_validate_missing_required_field(self) -> None:
        """Test ValidationError is raised when required field is missing."""
        response_data = {"id": 123}  # missing required 'name' field
        response = self._create_mock_response()
        error_prefix = "Invalid data structure"

        with pytest.raises(ValidationError) as exc_info:
            ResponseValidator.validate(
                response_data=response_data,
                response=response,
                model_cls=SampleModel,
                error_prefix=error_prefix,
            )

        assert "Invalid data structure:" in str(exc_info.value)
        assert exc_info.value.response == response
        assert isinstance(exc_info.value.__cause__, PydanticValidationError)

    def test_validate_wrong_data_type(self) -> None:
        """Test ValidationError is raised with wrong data type."""
        response_data = "invalid-string-data"  # should be dict for SampleModel
        response = self._create_mock_response()
        error_prefix = "Data type mismatch"

        with pytest.raises(ValidationError) as exc_info:
            ResponseValidator.validate(
                response_data=response_data,
                response=response,
                model_cls=SampleModel,
                error_prefix=error_prefix,
            )

        assert "Data type mismatch:" in str(exc_info.value)
        assert exc_info.value.response == response
        assert isinstance(exc_info.value.__cause__, PydanticValidationError)

    @pytest.mark.parametrize(
        "response_data,expected_id,expected_name",
        [
            ({"id": 1, "name": "First"}, 1, "First"),
            ({"id": 999, "name": "Last Item"}, 999, "Last Item"),
            ({"id": 0, "name": ""}, 0, ""),  # Edge case: empty string name
        ],
    )
    def test_validate_parametrized_success(
        self, response_data: dict[str, Any], expected_id: int, expected_name: str
    ) -> None:
        """Test successful validation with different valid data combinations."""
        response = self._create_mock_response()
        error_prefix = "Validation failed"

        result = ResponseValidator.validate(
            response_data=response_data,
            response=response,
            model_cls=SampleModel,
            error_prefix=error_prefix,
        )

        assert result.id == expected_id
        assert result.name == expected_name

    def test_validate_error_prefix_formatting(self) -> None:
        """Test that error prefix is correctly formatted in the exception message."""
        response_data = {"invalid": "data"}
        response = self._create_mock_response()
        custom_prefix = "Custom error prefix with special chars: [123]"

        with pytest.raises(ValidationError) as exc_info:
            ResponseValidator.validate(
                response_data=response_data,
                response=response,
                model_cls=SampleModel,
                error_prefix=custom_prefix,
            )

        # Verify the exact prefix format: "prefix: pydantic_error"
        error_message = str(exc_info.value)
        assert error_message.startswith(f"{custom_prefix}:")
        assert exc_info.value.response == response
