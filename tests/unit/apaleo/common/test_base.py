from dataclasses import dataclass
from typing import Any, cast
from unittest.mock import Mock

import pytest
from pydantic import BaseModel, Field, field_serializer
from pydantic_core import PydanticSerializationError

from apaleoapi.apaleo.common.base import BaseAdapter
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.enums import OperationOp
from apaleoapi.apaleo.common.schemas.payload import OperationModel
from apaleoapi.exceptions import ParameterSerializationError, PayloadSerializationError

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
