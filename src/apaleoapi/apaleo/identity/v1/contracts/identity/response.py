from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apaleoapi.apaleo.common.contracts.response import Count
from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo


@dataclass(frozen=True)
class Invitation:
    email: str
    is_account_admin: bool
    invited_by: str
    created: datetime
    properties: list[str] | None = None
    role: RoleInvitedTo | None = None
    roles: list[RoleAccessTo] | None = None


@dataclass(frozen=True)
class InvitedUserToAccountResponse:
    email: str


@dataclass(frozen=True)
class PropertyRolesItem:
    id: str
    roles: list[RoleAccessTo]


@dataclass(frozen=True)
class RoleList:
    items: list[RoleAccessTo]
    count: int


@dataclass(frozen=True)
class UserItem:
    subject_id: UUID
    first_name: str
    last_name: str
    email: str
    enabled: bool
    is_account_admin: bool
    is_mfa_enabled: bool
    is_passkeys_enabled: bool
    properties: list[PropertyRolesItem] | None = None


@dataclass(frozen=True)
class User:
    subject_id: UUID
    first_name: str
    last_name: str
    email: str
    is_account_admin: bool
    is_mfa_enabled: bool
    enabled: bool | None = None
    properties: list[str] | None = None
    property_roles: list[PropertyRolesItem] | None = None


@dataclass(frozen=True)
class UsersList:
    items: list[UserItem]
    count: int


@dataclass(frozen=True)
class InvitationList(Count):
    items: list[Invitation]
    count: int
