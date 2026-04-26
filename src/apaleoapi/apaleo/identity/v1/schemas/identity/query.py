from pydantic import EmailStr, Field

from apaleoapi.apaleo.common.schemas.base import BatchRequestBaseModel, StrictBaseModel
from apaleoapi.apaleo.identity.v1.enums.identity import UserSortBy


class InvitationListParamsModel(StrictBaseModel):
    property_id: str | None = Field(None, alias="propertyId")


class UserListParamsModel(BatchRequestBaseModel):
    property_ids: list[str] | None = Field(None, alias="propertyIds")
    email: EmailStr | None = Field(None)
    enabled: bool | None = Field(None)
    sort: UserSortBy | None = Field(None)
