from pydantic import EmailStr, Field

from apaleoapi.apaleo.identity.v1.enums.identity import UserSortBy
from apaleoapi.schemas import BatchRequestBaseModel, StrictBaseModel


class InvitationListParamsModel(StrictBaseModel):
    property_id: str | None = Field(None, alias="propertyId")


class UserListParamsModel(BatchRequestBaseModel):
    property_ids: list[str] | None = Field(None, alias="propertyIds")
    email: EmailStr | None = Field(None)
    enabled: bool | None = Field(None)
    sort: UserSortBy | None = Field(None)
