from uuid import UUID

from pydantic import AwareDatetime, Field

from apaleoapi.apaleo.common.schemas.base import ExtendedBaseModel, ListBaseModel
from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo


class InvitationModel(ExtendedBaseModel):
    email: str = Field(..., min_length=1)
    properties: list[str] | None = Field(None)
    is_account_admin: bool = Field(..., alias="isAccountAdmin")
    role: RoleInvitedTo | None = Field(None)
    roles: list[RoleAccessTo] | None = Field(None)
    invited_by: str = Field(..., alias="invitedBy", min_length=1)
    created: AwareDatetime = Field(...)


class InvitedUserToAccountResponseModel(ExtendedBaseModel):
    email: str = Field(..., min_length=1)


class PropertyRolesItemModel(ExtendedBaseModel):
    id: str = Field(..., min_length=1)
    roles: list[RoleAccessTo] = Field(...)


class RoleListModel(ExtendedBaseModel):
    roles: list[RoleAccessTo] = Field(...)


class UserItemModel(ExtendedBaseModel):
    subject_id: UUID = Field(..., alias="subjectId")
    first_name: str = Field(..., alias="firstName", min_length=1)
    last_name: str = Field(..., alias="lastName", min_length=1)
    email: str = Field(..., min_length=1)
    properties: list[PropertyRolesItemModel] | None = Field(None)
    enabled: bool = Field(...)
    is_account_admin: bool = Field(..., alias="isAccountAdmin")
    is_mfa_enabled: bool = Field(..., alias="isMfaEnabled")
    is_passkeys_enabled: bool = Field(..., alias="isPasskeysEnabled")


class UserModel(ExtendedBaseModel):
    subject_id: UUID = Field(..., alias="subjectId")
    first_name: str = Field(..., alias="firstName", min_length=1)
    last_name: str = Field(..., alias="lastName", min_length=1)
    email: str = Field(..., min_length=1)
    enabled: bool | None = Field(None)
    is_account_admin: bool = Field(..., alias="isAccountAdmin")
    is_mfa_enabled: bool = Field(..., alias="isMfaEnabled")
    properties: list[str] | None = Field(None)
    property_roles: list[PropertyRolesItemModel] | None = Field(None, alias="propertyRoles")


class UsersListModel(ListBaseModel[UserItemModel]):
    items: list[UserItemModel] = Field(default_factory=list, alias="users")


class InvitationListModel(ExtendedBaseModel):
    invitations: list[InvitationModel] = Field(default_factory=list)
