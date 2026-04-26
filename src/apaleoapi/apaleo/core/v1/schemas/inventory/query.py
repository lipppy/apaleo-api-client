from pydantic import Field

from apaleoapi.apaleo.common.schemas.base import BatchRequestBaseModel, StrictBaseModel


class PropertyListParamsModel(BatchRequestBaseModel):
    status: list[str] | None = None
    include_archived: bool | None = Field(None, alias="includeArchived")
    country_code: list[str] | None = Field(None, alias="countryCode")
    expand: list[str] | None = None


class PropertyGetParamsModel(StrictBaseModel):
    languages: list[str] | None = None
    expand: list[str] | None = None
