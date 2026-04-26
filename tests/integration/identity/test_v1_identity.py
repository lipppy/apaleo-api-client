import pytest

from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.identity.v1.apis.identity import IdentityV1IdentityAdapter
from apaleoapi.apaleo.identity.v1.identity import (
    CreateInvitation,
    InvitationList,
    InvitedUserToAccountResponse,
    RoleInvitedTo,
    RoleList,
    User,
    UsersList,
)
from apaleoapi.client import ApaleoAPIClient
from apaleoapi.exceptions import ForbiddenError, NotFoundError

pytestmark = [pytest.mark.integration, pytest.mark.live]


MOCK_EMAIL = "invalid-email-address@invalid.com"


class TestIdentityV1IdentityAdapter:
    """Integration tests for IdentityV1IdentityAdapter."""

    @pytest.fixture(autouse=True)
    def setup(self, client_valid: ApaleoAPIClient, client_invalid: ApaleoAPIClient) -> None:
        """Setup for each test method."""
        # This will be set by the test framework when the client fixture is injected
        self.adapter: IdentityV1IdentityAdapter = client_valid.identity.v1.identity
        self.adapter_invalid: IdentityV1IdentityAdapter = client_invalid.identity.v1.identity

    @pytest.mark.asyncio
    async def test_invitations(self) -> None:
        """Test the invitations flow: list, create, list again, delete, list again."""

        # 1. Lsit invitations
        invitations = await self.adapter.list_invitations()
        assert invitations is not None
        assert isinstance(invitations, InvitationList)
        assert isinstance(invitations.invitations, list)
        invitations_count = len(invitations.invitations)
        assert invitations_count >= 0

        # 2 Create invitation - None account admin, role Housekeeping, property BER
        payload = CreateInvitation(
            email=MOCK_EMAIL,
            properties=["BER"],
            is_account_admin=False,
            role=RoleInvitedTo.HOUSEKEEPING,
        )
        invited_user = await self.adapter.create_invitation(payload=payload)
        assert invited_user is not None
        assert isinstance(invited_user, InvitedUserToAccountResponse)
        assert invited_user.email == MOCK_EMAIL

        # 3. List invitations again and check the count increased by 1
        invitations_after = await self.adapter.list_invitations()
        assert invitations_after is not None
        assert isinstance(invitations_after, InvitationList)
        assert isinstance(invitations_after.invitations, list)
        assert len(invitations_after.invitations) == invitations_count + 1

        # 4. Cleanup, delete the created invitation
        await self.adapter.delete_invitation(email=MOCK_EMAIL)

        # 5. List invitations again and check the count is back to original
        invitations_final = await self.adapter.list_invitations()
        assert invitations_final is not None
        assert isinstance(invitations_final, InvitationList)
        assert isinstance(invitations_final.invitations, list)
        assert len(invitations_final.invitations) == invitations_count

    @pytest.mark.asyncio
    async def test_get_roles(self) -> None:
        """Test fetching roles."""
        roles = await self.adapter.list_roles()
        assert roles is not None
        assert isinstance(roles, RoleList)
        assert isinstance(roles.roles, list)
        assert len(roles.roles) >= 0

    @pytest.mark.asyncio
    async def test_users(self) -> None:
        """Test the users flow: list, get by ID, update, get again, revert update, get again."""

        # 1. List users
        users = await self.adapter.list_users()
        assert users is not None
        assert isinstance(users, UsersList)
        assert isinstance(users.items, list)
        assert users.count >= 0

        # 2. If there are users, get the first user by ID
        if users.count > 0:
            user_id = users.items[0].subject_id

            # 2.1. Get user by ID
            user = await self.adapter.get_user(user_id=str(user_id))
            assert user is not None
            assert isinstance(user, User)
            assert user.subject_id == user_id

            # 2.2. Update user
            await self.adapter.update_user(
                user_id=str(user_id),
                payload=[
                    Operation(
                        op="replace",
                        path="/enabled",
                        value=True,
                    )
                ],
            )

            # 2.3. Get user again and check the enabled status is updated
            user_after_update = await self.adapter.get_user(user_id=str(user_id))
            assert user_after_update is not None
            assert isinstance(user_after_update, User)
            assert user_after_update.subject_id == user_id
            assert user_after_update.enabled is True

            # 2.4. Revert the enabled status change to keep the test idempotent
            await self.adapter.update_user(
                user_id=str(user_id),
                payload=[
                    Operation(
                        op="replace",
                        path="/enabled",
                        value=True,
                    )
                ],
            )

            # 2.5. Get user again and check the enabled status is reverted back
            user_after_revert = await self.adapter.get_user(user_id=str(user_id))
            assert user_after_revert is not None
            assert isinstance(user_after_revert, User)
            assert user_after_revert.subject_id == user_id
            assert user_after_revert.enabled is True

    @pytest.mark.asyncio
    async def test_get_user_invalid_id(self) -> None:
        """Test getting a user with an invalid ID."""
        with pytest.raises(NotFoundError, match="The Request-URI could not be found."):
            _ = await self.adapter.get_user(user_id="invalid-user-id")

    @pytest.mark.asyncio
    async def test_get_current_user(self) -> None:
        """Test getting the current user which is forbidden with client credentials."""
        with pytest.raises(ForbiddenError, match="Forbidden."):
            _ = await self.adapter.get_current_user()
