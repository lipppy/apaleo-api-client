from typing import Any

from pydantic import Field

from apaleoapi.schemas import ExtendedBaseModel


class OperationModel(ExtendedBaseModel):
    value: Any | None = None
    path: str | None = None
    op: str | None = None
    from_: str | None = Field(None, alias="from")
