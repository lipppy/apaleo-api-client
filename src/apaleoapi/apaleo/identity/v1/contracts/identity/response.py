from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo


@dataclass(frozen=True)
class InvitationAuditLog:
    aggregate_type: str | None = None
    account_code: str | None = None
    email: str | None = None
    properties: list[str] | None = None
    roles: list[str] | None = None
    is_account_admin: bool | None = None


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
class PropertyRolesAuditLog:
    id: str | None = None
    roles: list[str] | None = None


@dataclass(frozen=True)
class PropertyRolesItem:
    id: str
    roles: list[RoleAccessTo]


@dataclass(frozen=True)
class RoleList:
    roles: list[RoleAccessTo]


@dataclass(frozen=True)
class UserAuditLog:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    enabled: bool | None = None
    is_account_admin: bool | None = None
    properties_roles: list[PropertyRolesAuditLog] | None = None
    aggregate_type: str | None = None


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
class InvitationList:
    invitations: list[Invitation]
