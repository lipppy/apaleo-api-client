from typing import Any

from pydantic import Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel


class OperationModel(ExtendedBaseModel):
    value: Any | None = None
    path: str | None = None
    op: str | None = None
    from_: str | None = Field(None, alias="from")
