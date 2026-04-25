import pytest

from apaleoapi.apaleo.identity.v1.apis.identity import IdentityV1IdentityAdapter
from apaleoapi.apaleo.identity.v1.contracts.identity.response import UsersList
from apaleoapi.client import ApaleoAPIClient

pytestmark = [pytest.mark.integration, pytest.mark.live]


class TestIdentityV1IdentityAdapter:
    """Integration tests for IdentityV1IdentityAdapter."""

    @pytest.fixture(autouse=True)
    def setup(self, client_valid: ApaleoAPIClient, client_invalid: ApaleoAPIClient) -> None:
        """Setup for each test method."""
        # This will be set by the test framework when the client fixture is injected
        self.adapter: IdentityV1IdentityAdapter = client_valid.identity.v1.identity
        self.adapter_invalid: IdentityV1IdentityAdapter = client_invalid.identity.v1.identity

    @pytest.mark.asyncio
    async def test_get_users(self) -> None:
        """Test fetching users."""
        users = await self.adapter.list_users()
        assert users is not None
        assert isinstance(users, UsersList)
        assert isinstance(users.items, list)
        assert users.count >= 0
