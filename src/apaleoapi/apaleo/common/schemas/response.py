from pydantic import Field

from apaleoapi.schemas import ExtendedBaseModel


class MessageItemCollection(ExtendedBaseModel):
    messages: list[str] | None = None


class CountModel(ExtendedBaseModel):
    count: int = Field(0, description="Total count of items matching the query")
