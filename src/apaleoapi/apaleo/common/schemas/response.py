from apaleoapi.schemas import ExtendedBaseModel


class MessageItemCollection(ExtendedBaseModel):
    messages: list[str] | None = None
