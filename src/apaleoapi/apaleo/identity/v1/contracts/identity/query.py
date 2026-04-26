from dataclasses import dataclass

from apaleoapi.apaleo.common.contracts.base import BatchRequest
from apaleoapi.apaleo.identity.v1.enums.identity import UserSortBy


@dataclass(frozen=True)
class InvitationListParams:
    property_id: str | None = None


@dataclass
class UserListParams(BatchRequest):
    property_ids: list[str] | None = None
    email: str | None = None
    enabled: bool | None = None
    sort: UserSortBy | None = None
