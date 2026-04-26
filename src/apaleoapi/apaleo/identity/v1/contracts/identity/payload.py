from dataclasses import dataclass

from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo


@dataclass(frozen=True)
class CreateInvitation:
    email: str
    properties: list[str] | None = None
    is_account_admin: bool | None = None
    roles: list[RoleAccessTo] | None = None
    role: RoleInvitedTo | None = None
