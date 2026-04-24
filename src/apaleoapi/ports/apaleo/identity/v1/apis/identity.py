"""
Apaleo Identity V1 Identity API Port

See: https://identity.apaleo.com/swagger/index.html?urls.primaryName=Identity+V1
"""

from typing import Protocol

from apaleoapi.apaleo.identity.v1.contracts.identity.payloads import CreateInvitation
from apaleoapi.apaleo.identity.v1.contracts.identity.queries import InvitationListParams
from apaleoapi.apaleo.identity.v1.contracts.identity.responses import (
    InvitationList,
    InvitedUserToAccountResponse,
    RoleList,
    User,
    UsersList,
)


class IdentityV1IdentityPort(Protocol):
    _path: str = "api"
    _version: str

    # Invitation methods

    async def list_invitations(self, params: InvitationListParams | None = None) -> InvitationList:
        """List invitations for the current account."""
        pass

    async def create_invitation(self, payload: CreateInvitation) -> InvitedUserToAccountResponse:
        """Create an invitation to the current account."""
        pass

    async def delete_invitation(self, email: str) -> None:
        """Delete an invitation by email if it exists."""
        pass

    # Roles methods

    async def list_roles(self) -> RoleList:
        """List all roles."""
        pass

    # Users methods

    async def list_users(self) -> UsersList:
        """List all users."""
        pass

    async def get_user(self, user_id: str) -> User:
        """Get a user by user ID (subject ID)."""
        pass

    async def update_user(self, user_id: str) -> None:
        """Update a user by user ID (subject ID)."""
        pass

    async def get_current_user(self) -> User:
        """Get the current user."""
        pass
