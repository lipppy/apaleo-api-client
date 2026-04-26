from pydantic import EmailStr, Field

from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo
from apaleoapi.schemas import ExtendedBaseModel


class CreateInvitationModel(ExtendedBaseModel):
    email: EmailStr = Field(..., min_length=1)
    properties: list[str] | None = Field(None)
    is_account_admin: bool | None = Field(None, alias="isAccountAdmin")
    roles: list[RoleAccessTo] | None = Field(None)
    role: RoleInvitedTo | None = Field(None)
