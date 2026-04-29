"""
Apaleo Identity Identity API Adapter.

This module contains the implementation of the IdentityPort interface
to interact with the Apaleo Identity API.

See: https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1
"""

from apaleoapi.apaleo.common.base import BaseAdapter
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.schemas.payload import OperationModel
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
    InvitationList,
    InvitedUserToAccountResponse,
    RoleList,
    User,
    UsersList,
)
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
    InvitedUserToAccountResponseModel,
    RoleListModel,
    UserModel,
    UsersListModel,
)
from apaleoapi.logging import get_logger
from apaleoapi.ports.apaleo.identity.v1.apis.identity import IdentityV1IdentityResourcePort
from apaleoapi.ports.http.transport import AsyncTransportPort

log = get_logger(__name__)


class IdentityV1IdentityResource(BaseAdapter, IdentityV1IdentityResourcePort):
    """Adapter for Identity V1 Identity API endpoints."""

    def __init__(self, transport: AsyncTransportPort, max_concurrent: int, dry_run: bool = False):
        super().__init__(transport=transport, max_concurrent=max_concurrent, dry_run=dry_run)
        self._version = "v1"
        self._base_path = f"{self._path}/{self._version}"

    # Invitation methods

    async def list_invitations(self, params: InvitationListParams | None = None) -> InvitationList:
        """List invitations for the current account."""
        url = f"{self._base_path}/account/invitations"

        return await self._get_resource(
            url=url,
            params=params,
            params_model_cls=InvitationListParamsModel,
            model_cls=InvitationListModel,
            faker_factory=InvitationListFakerFactory,
            default_factory=InvitationListModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to list invitations for the current account",
            return_cls=InvitationList,
        )

    async def create_invitation(self, payload: CreateInvitation) -> InvitedUserToAccountResponse:
        """Create an invitation to the current account."""
        url = f"{self._base_path}/account/invitations"

        return await self._post_resource(
            url=url,
            payload=payload,
            payload_model_cls=CreateInvitationModel,
            model_cls=InvitedUserToAccountResponseModel,
            faker_factory=InvitedUserToAccountResponseFakerFactory,
            default_factory=InvitedUserToAccountResponseModelDefaultFactory,
            success_codes={200},
            error_prefix="Failed to create an invitation for the current account",
            return_cls=InvitedUserToAccountResponse,
        )

    async def delete_invitation(self, email: str) -> None:
        """Delete an invitation by email if it exists."""
        url = f"{self._base_path}/account/invitations/{email}"

        await self._delete_resource(url=url)

    # Roles methods

    async def list_roles(self) -> RoleList:
        """List all roles."""
        url = f"{self._base_path}/roles"

        return await self._get_resource(
            url=url,
            model_cls=RoleListModel,
            faker_factory=RoleListFakerFactory,
            default_factory=RoleListModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to list roles for the current account",
            return_cls=RoleList,
        )

    # Users methods

    async def list_users(self, params: UserListParams | None = None) -> UsersList:
        """List all users for the current account."""
        url = f"{self._base_path}/users"

        return await self._get_resource_concurrently(
            url=url,
            params=params,
            params_model_cls=UserListParamsModel,
            model_cls=UsersListModel,
            faker_factory=UsersListFakerFactory,
            default_factory=UsersListModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to list users for the current account",
            return_cls=UsersList,
        )

    async def get_user(self, user_id: str) -> User:
        """Get a user by user ID (subject ID)."""
        url = f"{self._base_path}/users/{user_id}"

        return await self._get_resource(
            url=url,
            model_cls=UserModel,
            faker_factory=UserFakerFactory,
            default_factory=UserModelDefaultFactory,
            success_codes={200, 204},
            error_prefix=f"Failed to get user with ID {user_id} for the current account",
            return_cls=User,
        )

    async def update_user(self, user_id: str, payload: list[Operation]) -> None:
        """Update a user by user ID (subject ID)."""
        url = f"{self._base_path}/users/{user_id}"

        await self._patch_resource(
            url=url,
            payload=payload,
            payload_model_cls=OperationModel,
            error_prefix=f"Failed to update user with ID {user_id}",
        )

    async def get_current_user(self) -> User:
        """Get the current user."""
        url = f"{self._base_path}/users/me"

        return await self._get_resource(
            url=url,
            model_cls=UserModel,
            faker_factory=UserFakerFactory,
            default_factory=UserModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to get the current user for the current account",
            return_cls=User,
        )
