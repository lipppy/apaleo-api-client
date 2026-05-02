"""Apaleo Identity API - Identity V1.

Centralized module for Identity V1 with convenient imports
for all dataclasses, enums, and parameters.

Usage:
    # Import specific entities
    from apaleoapi.apaleo.identity.v1.identity import User, UsersList, RoleAccessTo

    # Or import from sub-modules for organization
    from apaleoapi.apaleo.identity.v1.enums import RoleAccessTo
    from apaleoapi.apaleo.identity.v1.contracts.identity.response import User
"""

from apaleoapi.apaleo.identity.v1.contracts.identity.factory import (
    InvitationListFakerFactory,
    InvitedUserToAccountResponseFakerFactory,
    RoleListFakerFactory,
    UserFakerFactory,
    UsersListFakerFactory,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.payload import CreateInvitation
from apaleoapi.apaleo.identity.v1.contracts.identity.query import (
    InvitationListParams,
    UserListParams,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.response import (
    Invitation,
    InvitationList,
    InvitedUserToAccountResponse,
    PropertyRolesItem,
    RoleList,
    User,
    UserItem,
    UsersList,
)
from apaleoapi.apaleo.identity.v1.enums.identity import RoleAccessTo, RoleInvitedTo, UserSortBy
from apaleoapi.apaleo.identity.v1.schemas.identity.factory import (
    InvitationListModelDefaultFactory,
    InvitedUserToAccountResponseModelDefaultFactory,
    RoleListModelDefaultFactory,
    UserModelDefaultFactory,
    UsersListModelDefaultFactory,
)
from apaleoapi.apaleo.identity.v1.schemas.identity.payload import CreateInvitationModel
from apaleoapi.apaleo.identity.v1.schemas.identity.query import (
    InvitationListParamsModel,
    UserListParamsModel,
)
from apaleoapi.apaleo.identity.v1.schemas.identity.response import (
    InvitationListModel,
    InvitationModel,
    InvitedUserToAccountResponseModel,
    PropertyRolesItemModel,
    RoleListModel,
    UserItemModel,
    UserModel,
    UsersListModel,
)

__all__ = [
    # Dataclasses - Common
    # Dataclasses - Response
    "User",
    "UserItem",
    "UsersList",
    "Invitation",
    "InvitationList",
    "InvitedUserToAccountResponse",
    "PropertyRolesItem",
    "RoleList",
    # Dataclasses - Payload
    "CreateInvitation",
    # Dataclasses - Query Parameters
    "InvitationListParams",
    "UserListParams",
    # Dataclasses - Factories
    "RoleListFakerFactory",
    "UserFakerFactory",
    "UsersListFakerFactory",
    "InvitationListFakerFactory",
    "InvitedUserToAccountResponseFakerFactory",
    # Enums
    "RoleAccessTo",
    "RoleInvitedTo",
    "UserSortBy",
    # Schemas - Common
    # Schemas - Response
    "UserModel",
    "UserItemModel",
    "UsersListModel",
    "InvitationModel",
    "InvitationListModel",
    "InvitedUserToAccountResponseModel",
    "PropertyRolesItemModel",
    "RoleListModel",
    # Schemas - Payload
    "CreateInvitationModel",
    # Schemas - Query Parameters
    "InvitationListParamsModel",
    "UserListParamsModel",
    # Schemas - Factories
    "UserModelDefaultFactory",
    "UsersListModelDefaultFactory",
    "InvitationListModelDefaultFactory",
    "InvitedUserToAccountResponseModelDefaultFactory",
    "RoleListModelDefaultFactory",
]
