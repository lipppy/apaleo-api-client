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
from apaleoapi.apaleo.identity.v1.factories.identity import (
    InvitationListModelDefaultFactory,
    InvitationListModelFakerFactory,
    InvitedUserToAccountResponseModelDefaultFactory,
    InvitedUserToAccountResponseModelFakerFactory,
    RoleListModelDefaultFactory,
    RoleListModelFakerFactory,
    UserModelDefaultFactory,
    UserModelFakerFactory,
    UsersListModelDefaultFactory,
    UsersListModelFakerFactory,
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
    # Enums
    "RoleAccessTo",
    "RoleInvitedTo",
    "UserSortBy",
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
    # Factories
    "UserModelDefaultFactory",
    "UsersListModelDefaultFactory",
    "InvitationListModelDefaultFactory",
    "InvitedUserToAccountResponseModelDefaultFactory",
    "RoleListModelDefaultFactory",
    "RoleListModelFakerFactory",
    "UserModelFakerFactory",
    "UsersListModelFakerFactory",
    "InvitationListModelFakerFactory",
    "InvitedUserToAccountResponseModelFakerFactory",
]
