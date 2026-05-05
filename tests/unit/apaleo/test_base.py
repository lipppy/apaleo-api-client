import re
from dataclasses import dataclass
from typing import Any, cast
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from pydantic import BaseModel, Field, field_serializer
from pydantic_core import PydanticSerializationError

from apaleoapi.apaleo.base import BaseAdapter
from apaleoapi.apaleo.common.contracts.base import BatchRequest
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.enums import OperationOp
from apaleoapi.apaleo.common.schemas.base import BatchRequestBaseModel, ListBaseModel
from apaleoapi.apaleo.common.schemas.payload import OperationModel
from apaleoapi.exceptions import (
    APIError,
    BadRequestError,
    InternalServerError,
    ParameterSerializationError,
    PayloadSerializationError,
)
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.validation.url_path_validator import URLPathValidator

pytestmark = [pytest.mark.unit]


@dataclass
class SampleParams:
    property_id: str
    page_number: int | None = None


class SampleParamsModel(BaseModel):
    """Model with non-aliased fields for params serialization tests."""

    property_id: str
    page_number: int | None = None


class AliasedParamsModel(BaseModel):
    """Model with aliased fields for params serialization tests."""

    property_id: str = Field(..., alias="propertyId")
    page_number: int | None = Field(None, alias="pageNumber")

    model_config = {"populate_by_name": True}


class ParamsWithFailingSerializerModel(BaseModel):
    params: Any

    @field_serializer("params")
    def serialize_params(self, value: Any) -> Any:
        raise PydanticSerializationError("params serialization failed")


@dataclass
class SamplePayload:
    property_id: str
    is_active: bool = True


class SamplePayloadModel(BaseModel):
    """Model with non-aliased fields for payload serialization tests."""

    property_id: str
    is_active: bool = True


class AliasedPayloadModel(BaseModel):
    """Model with aliased fields for payload serialization tests."""

    property_id: str = Field(alias="propertyId")
    is_active: bool = Field(default=True, alias="isActive")

    model_config = {"populate_by_name": True}


class PayloadWithFailingSerializerModel(BaseModel):
    payload: Any

    @field_serializer("payload")
    def serialize_payload(self, value: Any) -> Any:
        raise PydanticSerializationError("payload serialization failed")


class PatchPayloadWithFailingSerializerModel(BaseModel):
    operation: Any

    @field_serializer("operation")
    def serialize_operation(self, value: Any) -> Any:
        raise PydanticSerializationError("patch payload serialization failed")


@dataclass
class SampleBatchParams(BatchRequest):
    some_param: str | None = None


class SampleBatchParamsModel(BatchRequestBaseModel):
    some_param: str | None = Field(None, alias="someParam")


@dataclass
class SampleListItem:
    id: str


@dataclass
class SampleListResponse:
    items: list[SampleListItem]
    count: int


class SampleListItemModel(BaseModel):
    id: str


class SampleListModel(ListBaseModel[SampleListItemModel]):
    pass


class SampleListDefaultFactory:
    @staticmethod
    def build() -> SampleListModel:
        return SampleListModel(items=[], count=0)


class SampleListFakerFactory:
    def build(self) -> SampleListResponse:
        return SampleListResponse(items=[], count=0)


class TestBaseAdapterSerializeParams:
    """Test cases for BaseAdapter._serialize_params."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.adapter = BaseAdapter(transport=Mock(), max_concurrent=2)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("params", "params_model_cls", "expected"),
        [
            (
                SampleParams(property_id="BER", page_number=None),
                SampleParamsModel,
                {"property_id": "BER"},
            ),
            (
                {"property_id": "BER", "page_number": 2},
                SampleParamsModel,
                {"property_id": "BER", "page_number": 2},
            ),
            (
                {"property_id": "BER", "pageNumber": 2},
                AliasedParamsModel,
                {"propertyId": "BER", "pageNumber": 2},
            ),
            ({"property_id": "BER"}, None, {}),
        ],
    )
    async def test_serialize_params_success_cases(
        self,
        params: SampleParams | dict[str, Any],
        params_model_cls: type[BaseModel] | None,
        expected: dict[str, Any],
    ) -> None:
        """Test successful params serialization for supported input shapes."""
        result = await self.adapter._serialize_params(params, params_model_cls)

        assert result == expected

    @pytest.mark.asyncio
    async def test_serialize_params_raises_parameter_serialization_error_for_invalid_type(
        self,
    ) -> None:
        """Test validation errors are wrapped for params serialization."""
        with pytest.raises(ParameterSerializationError) as exc_info:
            await self.adapter._serialize_params(cast(Any, "invalid"), SampleParamsModel)

        assert "Failed to validate query parameters" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_serialize_params_raises_parameter_serialization_error_on_validation(
        self,
    ) -> None:
        """Test validation errors are wrapped for params serialization."""
        with pytest.raises(ParameterSerializationError) as exc_info:
            await self.adapter._serialize_params({"page_number": "invalid"}, SampleParamsModel)

        assert "Failed to validate query parameters" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_serialize_params_raises_parameter_serialization_error_on_dump(self) -> None:
        """Test serialization errors are wrapped for params serialization."""
        with pytest.raises(ParameterSerializationError) as exc_info:
            await self.adapter._serialize_params(
                {"params": object()}, ParamsWithFailingSerializerModel
            )

        assert "Failed to serialize query parameters" in str(exc_info.value)


class TestBaseAdapterSerializePayload:
    """Test cases for BaseAdapter._serialize_payload."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.adapter = BaseAdapter(transport=Mock(), max_concurrent=2)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("payload", "payload_model_cls", "expected"),
        [
            (
                SamplePayload(property_id="BER"),
                SamplePayloadModel,
                {"property_id": "BER", "is_active": True},
            ),
            (
                {"property_id": "BER", "is_active": False},
                AliasedPayloadModel,
                {"propertyId": "BER", "isActive": False},
            ),
            (
                {"property_id": "BER", "isActive": False},
                AliasedPayloadModel,
                {"propertyId": "BER", "isActive": False},
            ),
        ],
    )
    async def test_serialize_payload_success_cases(
        self,
        payload: SamplePayload | dict[str, Any],
        payload_model_cls: type[BaseModel],
        expected: dict[str, Any],
    ) -> None:
        """Test successful payload serialization for supported input shapes."""
        result = await self.adapter._serialize_payload(payload, payload_model_cls)

        assert result == expected

    @pytest.mark.asyncio
    async def test_serialize_payload_raises_payload_serialization_error_for_invalid_type(
        self,
    ) -> None:
        """Test invalid payload types are rejected."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_payload(cast(Any, "invalid"), SamplePayloadModel)

        assert "Payload must be a dataclass instance or a dictionary" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_serialize_payload_raises_payload_serialization_error_on_validation(
        self,
    ) -> None:
        """Test validation errors are wrapped for payload serialization."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_payload({"property_id": 123}, SamplePayloadModel)

        assert "Failed to validate payload" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_serialize_payload_raises_payload_serialization_error_on_dump(self) -> None:
        """Test serialization errors are wrapped for payload serialization."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_payload(
                {"payload": object()}, PayloadWithFailingSerializerModel
            )

        assert "Failed to serialize payload" in str(exc_info.value)


class TestBaseAdapterSerializePatchPayload:
    """Test cases for BaseAdapter._serialize_patch_payload."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.adapter = BaseAdapter(transport=Mock(), max_concurrent=2)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("payload", "expected"),
        [
            (
                [
                    Operation(
                        op=OperationOp.REPLACE,
                        path="/name",
                        value="Updated Hotel",
                    )
                ],
                [{"op": "replace", "path": "/name", "value": "Updated Hotel"}],
            ),
            (
                [
                    {
                        "op": OperationOp.MOVE,
                        "path": "/destination",
                        "from_": "/source",
                    }
                ],
                [{"op": "move", "path": "/destination", "from": "/source"}],
            ),
            (
                [
                    {
                        "op": "copy",
                        "path": "/destination",
                        "from": "/source",
                    }
                ],
                [{"op": "copy", "path": "/destination", "from": "/source"}],
            ),
        ],
    )
    async def test_serialize_patch_payload_success_cases(
        self,
        payload: list[Operation] | list[dict[str, Any]],
        expected: list[dict[str, Any]],
    ) -> None:
        """Test successful patch payload serialization for supported input shapes."""
        result = await self.adapter._serialize_patch_payload(
            payload, payload_model_cls=OperationModel
        )

        assert result == expected

    @pytest.mark.asyncio
    async def test_serialize_patch_payload_raises_payload_serialization_error_for_invalid_item_type(
        self,
    ) -> None:
        """Test invalid patch payload item types are rejected."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_patch_payload(
                cast(Any, ["invalid"]), payload_model_cls=OperationModel
            )

        assert "Each item in the payload list must be a dataclass instance or a dictionary" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_serialize_patch_payload_raises_payload_serialization_error_on_validation(
        self,
    ) -> None:
        """Test validation errors are wrapped for patch payload serialization."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_patch_payload(
                [{"path": 123, "op": OperationOp.REPLACE}], payload_model_cls=OperationModel
            )

        assert "Failed to validate payload item" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_serialize_patch_payload_raises_payload_serialization_error_on_dump(self) -> None:
        """Test serialization errors are wrapped for patch payload serialization."""
        with pytest.raises(PayloadSerializationError) as exc_info:
            await self.adapter._serialize_patch_payload(
                [{"operation": object()}], payload_model_cls=PatchPayloadWithFailingSerializerModel
            )

        assert "Failed to serialize payload item" in str(exc_info.value)


class TestBaseAdapterHeadResource:
    """Test cases for BaseAdapter._head_resource."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.transport = Mock(spec=AuthenticatedTransport)
        self.transport.request = AsyncMock()
        # Adapter without dry run mode to test the full flow including transport calls
        self.adapter = BaseAdapter(transport=self.transport, max_concurrent=2)
        self.adapter._url_path_validator = Mock(spec=URLPathValidator)
        self.adapter._url_path_validator.validate = Mock(side_effect=lambda url: f"validated/{url}")

        # Adapter with dry run mode to test short-circuiting before transport calls
        self.adapter_dry_run = BaseAdapter(transport=self.transport, max_concurrent=2, dry_run=True)
        self.adapter_dry_run._url_path_validator = Mock(spec=URLPathValidator)
        self.adapter_dry_run._url_path_validator.validate = Mock(
            side_effect=lambda url: f"validated/{url}"
        )

    @pytest.mark.asyncio
    async def test_head_resource_returns_true_for_success_status(self) -> None:
        """Test HEAD returns True when the resource exists."""
        self.transport.request.return_value = Mock(status_code=200)

        result = await self.adapter._head_resource(
            url="api/v1/resources/BER",
            error_prefix="Failed to check resource",
        )

        assert result is True
        self.transport.request.assert_awaited_once_with("HEAD", "validated/api/v1/resources/BER")

    @pytest.mark.asyncio
    async def test_head_resource_returns_false_for_not_found(self) -> None:
        """Test HEAD returns False when the resource is missing."""
        self.transport.request.return_value = Mock(status_code=404)

        result = await self.adapter._head_resource(
            url="api/v1/resources/MISSING",
            error_prefix="Failed to check resource",
        )

        assert result is False
        self.transport.request.assert_awaited_once_with(
            "HEAD", "validated/api/v1/resources/MISSING"
        )

    @pytest.mark.asyncio
    async def test_head_resource_returns_true_and_skips_transport_in_dry_run(self) -> None:
        """Test dry-run mode short-circuits after URL validation."""
        result = await self.adapter_dry_run._head_resource(
            url="api/v1/resources/BER",
            error_prefix="Failed to check resource",
        )

        assert result is True
        self.transport.request.assert_not_awaited()

    @pytest.mark.parametrize(
        ("status_code", "response_json", "expected_exception", "match"),
        [
            (
                201,
                b'{"unexpected": "response"}',
                APIError,
                (
                    "Failed to check resource: Unexpected response (201) for "
                    "HEAD request to validated/api/v1/resources/BER."
                ),
            ),
            (
                400,
                None,
                BadRequestError,
                "Bad request.",
            ),
            (
                419,
                None,
                APIError,
                "Unexpected status code: 419",
            ),
            (
                422,
                {"messages": ["Invalid propertyId."]},
                APIError,
                (
                    "Validation errors in the request body or query params. "
                    "Details: Invalid propertyId."
                ),
            ),
            (
                500,
                None,
                InternalServerError,
                "An unexpected error occurred.",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_head_resource_raises_error_for_unexpected_unhandled_status(
        self, status_code: int, response_json: bytes, expected_exception: type[APIError], match: str
    ) -> None:
        """Test adapter raises a generic APIError when the response handler does not."""
        response = Mock(
            spec=httpx.Response,
            status_code=status_code,
            headers={"content-type": "application/json"},
            text="Error or unexpected response",
        )
        self.transport.request.return_value = response
        if response_json is not None:
            response.json = Mock(return_value=response_json)

        with pytest.raises(expected_exception, match=re.escape(match)) as exc_info:
            await self.adapter._head_resource(
                url="api/v1/resources/BER",
                error_prefix="Failed to check resource",
            )

        assert exc_info.value.response is response
        self.transport.request.assert_awaited_once_with("HEAD", "validated/api/v1/resources/BER")


class TestBaseAdapterGetResourceConcurrently:
    """Test cases for BaseAdapter._get_resource_concurrently."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.transport = Mock()
        self.transport.request = AsyncMock()
        self.adapter = BaseAdapter(transport=self.transport, max_concurrent=2)
        cast(Any, self.adapter._response_handler).handle = Mock(
            side_effect=lambda response: response.payload
        )
        cast(Any, self.adapter._response_validator).validate = Mock(
            side_effect=lambda response_data, response, model_cls, error_prefix: (
                model_cls.model_validate(response_data)
            )
        )
        cast(Any, self.adapter._url_path_validator).validate = Mock(side_effect=lambda url: url)

    @pytest.mark.asyncio
    async def test_get_resource_concurrently_fetches_only_expected_pages_for_exact_division(
        self,
    ) -> None:
        """Test the concurrent branch does not request an extra page when count divides evenly."""

        async def request_side_effect(
            method: str, url: str, params: dict[str, Any] | None = None
        ) -> Mock:
            assert method == "GET"
            assert url == "api/v1/test"
            page_number = cast(int, params.get("pageNumber") if params else None)
            page_size = cast(int, params.get("pageSize") if params else None)
            payloads = {
                (1, 1): {"items": [{"id": "1"}], "count": 4},
                (1, 2): {"items": [{"id": "1"}, {"id": "2"}], "count": 4},
                (2, 2): {"items": [{"id": "3"}, {"id": "4"}], "count": 4},
            }
            if (page_number, page_size) not in payloads:
                raise AssertionError(f"Unexpected page request: {(page_number, page_size)}")

            return Mock(status_code=200, payload=payloads[(page_number, page_size)])

        self.transport.request.side_effect = request_side_effect

        result = await self.adapter._get_resource_concurrently(
            url="api/v1/test",
            params=SampleBatchParams(batch_size=2, is_concurrently=True),
            params_model_cls=cast(Any, SampleBatchParamsModel),
            model_cls=cast(Any, SampleListModel),
            faker_factory=cast(Any, SampleListFakerFactory),
            default_factory=cast(Any, SampleListDefaultFactory),
            return_cls=SampleListResponse,
            success_codes={200},
            error_prefix="Failed to fetch test resources",
        )

        assert self.transport.request.await_count == 1 + 2  # 1 for count, 2 for pages
        assert result.count == 4
        assert [item.id for item in result.items] == ["1", "2", "3", "4"]

    @pytest.mark.asyncio
    async def test_get_resource_concurrently_fetches_only_expected_pages_for_short_pages(
        self,
    ) -> None:
        """
        Test the concurrent branch continues fetching pages until all
        items are retrieved, even if some pages are short.
        """

        async def request_side_effect(
            method: str, url: str, params: dict[str, Any] | None = None
        ) -> Mock:
            assert method == "GET"
            assert url == "api/v1/test"
            page_number = cast(int, params.get("pageNumber") if params else None)
            page_size = cast(int, params.get("pageSize") if params else None)
            payloads = {
                (1, 1): {"items": [{"id": "1"}], "count": 5},
                (1, 2): {"items": [{"id": "1"}, {"id": "2"}], "count": 5},
                (2, 2): {"items": [{"id": "3"}, {"id": "4"}], "count": 5},
                (3, 2): {"items": [{"id": "5"}], "count": 5},
            }
            if (page_number, page_size) not in payloads:
                raise AssertionError(f"Unexpected page request: {(page_number, page_size)}")

            return Mock(status_code=200, payload=payloads[(page_number, page_size)])

        self.transport.request.side_effect = request_side_effect

        result = await self.adapter._get_resource_concurrently(
            url="api/v1/test",
            params=SampleBatchParams(batch_size=2, is_concurrently=True),
            params_model_cls=cast(Any, SampleBatchParamsModel),
            model_cls=cast(Any, SampleListModel),
            faker_factory=cast(Any, SampleListFakerFactory),
            default_factory=cast(Any, SampleListDefaultFactory),
            return_cls=SampleListResponse,
            success_codes={200},
            error_prefix="Failed to fetch test resources",
        )

        assert self.transport.request.await_count == 1 + 3  # 1 for count, 3 for pages
        assert result.count == 5
        assert [item.id for item in result.items] == ["1", "2", "3", "4", "5"]

    @pytest.mark.asyncio
    async def test_get_resource_concurrently_no_results(
        self,
    ) -> None:
        """Test the concurrent branch handles no results correctly."""

        async def request_side_effect(
            method: str, url: str, params: dict[str, Any] | None = None
        ) -> Mock:
            assert method == "GET"
            assert url == "api/v1/test"
            page_number = cast(int, params.get("pageNumber") if params else None)
            page_size = cast(int, params.get("pageSize") if params else None)
            payloads = {
                (1, 1): {"items": [], "count": 0},
            }
            if (page_number, page_size) not in payloads:
                raise AssertionError(f"Unexpected page request: {(page_number, page_size)}")

            return Mock(status_code=200, payload=payloads[(page_number, page_size)])

        self.transport.request.side_effect = request_side_effect

        result = await self.adapter._get_resource_concurrently(
            url="api/v1/test",
            params=SampleBatchParams(batch_size=10, is_concurrently=True),
            params_model_cls=cast(Any, SampleBatchParamsModel),
            model_cls=cast(Any, SampleListModel),
            faker_factory=cast(Any, SampleListFakerFactory),
            default_factory=cast(Any, SampleListDefaultFactory),
            return_cls=SampleListResponse,
            success_codes={200},
            error_prefix="Failed to fetch test resources",
        )

        assert self.transport.request.await_count == 1  # 1 for count, no pages since no results
        assert result.count == 0
        assert [item.id for item in result.items] == []


class TestBaseAdapterDeleteResource:
    """Test cases for BaseAdapter._delete_resource."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.transport = Mock(spec=AuthenticatedTransport)
        self.transport.request = AsyncMock()

        self.adapter = BaseAdapter(transport=self.transport, max_concurrent=2)
        self.adapter._url_path_validator = Mock(spec=URLPathValidator)
        self.adapter._url_path_validator.validate = Mock(side_effect=lambda url: f"validated/{url}")

        self.adapter_dry_run = BaseAdapter(transport=self.transport, max_concurrent=2, dry_run=True)
        self.adapter_dry_run._url_path_validator = Mock(spec=URLPathValidator)
        self.adapter_dry_run._url_path_validator.validate = Mock(
            side_effect=lambda url: f"validated/{url}"
        )

    @pytest.mark.asyncio
    async def test_delete_resource_returns_none_for_no_content_response(self) -> None:
        """Test DELETE succeeds for the expected 204 response."""
        self.transport.request.return_value = Mock(status_code=204)

        result = await self.adapter._delete_resource(
            url="api/v1/resources/BER",
        )  # type: ignore[func-returns-value]

        assert result is None
        self.transport.request.assert_awaited_once_with("DELETE", "validated/api/v1/resources/BER")

    @pytest.mark.asyncio
    async def test_delete_resource_skips_transport_in_dry_run(self) -> None:
        """Test dry-run mode short-circuits after URL validation."""
        result = await self.adapter_dry_run._delete_resource(
            url="api/v1/resources/BER",
        )  # type: ignore[func-returns-value]

        assert result is None
        self.transport.request.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_resource_tolerates_unexpected_success_payload_and_status(self) -> None:
        """Test DELETE logs warnings but still succeeds when no handler error is raised."""
        response = Mock(
            spec=httpx.Response, status_code=200, headers={"content-type": "application/json"}
        )
        response.json = Mock(return_value={"deleted": True})
        self.transport.request.return_value = response
        warning_msg_1 = (
            "DELETE request to validated/api/v1/resources/BER returned unexpected data: "
            "{'deleted': True}"
        )
        warning_msg_2 = (
            "DELETE request to validated/api/v1/resources/BER returned unexpected status code: 200"
        )

        with patch("apaleoapi.apaleo.base.log.warning") as warning_mock:
            result = await self.adapter._delete_resource(
                url="api/v1/resources/BER",
            )  # type: ignore[func-returns-value]

        assert result is None
        self.transport.request.assert_awaited_once_with("DELETE", "validated/api/v1/resources/BER")

        warning_mock.assert_any_call(warning_msg_1)
        warning_mock.assert_any_call(warning_msg_2)

    @pytest.mark.parametrize(
        ("status_code", "response_json", "expected_exception", "match"),
        [
            (400, None, BadRequestError, "Bad request."),
            (419, None, APIError, "Unexpected status code: 419"),
        ],
    )
    @pytest.mark.asyncio
    async def test_delete_resource_propagates_response_handler_errors(
        self,
        status_code: int,
        response_json: bytes | dict[str, Any] | None,
        expected_exception: type[APIError],
        match: str,
    ) -> None:
        """Test DELETE propagates API errors raised by the response handler."""
        response = Mock(
            spec=httpx.Response,
            status_code=status_code,
            headers={"content-type": "application/json"},
            text="Error response",
        )
        self.transport.request.return_value = response
        if response_json is not None:
            response.json = Mock(return_value=response_json)

        with pytest.raises(expected_exception, match=re.escape(match)) as exc_info:
            await self.adapter._delete_resource("api/v1/resources/BER")

        assert exc_info.value.response is response
        self.transport.request.assert_awaited_once_with("DELETE", "validated/api/v1/resources/BER")
