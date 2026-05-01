import pytest

from apaleoapi import ApaleoAPIClient
from apaleoapi.apaleo.core.v1.apis.inventory import CoreV1InventoryResource
from apaleoapi.apaleo.core.v1.contracts.inventory.payload import CreateAddress, CreateProperty
from apaleoapi.apaleo.core.v1.contracts.inventory.response import Property, PropertyList

pytestmark = [pytest.mark.integration, pytest.mark.live]


MOCK_EMAIL = "invalid-email-address@invalid.com"


class TestCoreV1InventoryResource:
    """Integration tests for CoreV1InventoryResource."""

    @pytest.fixture(autouse=True)
    def setup(self, client_valid: ApaleoAPIClient, client_invalid: ApaleoAPIClient) -> None:
        """Setup for each test method."""
        # This will be set by the test framework when the client fixture is injected
        self.adapter: CoreV1InventoryResource = client_valid.core.v1.inventory
        self.adapter_invalid: CoreV1InventoryResource = client_invalid.core.v1.inventory

    @pytest.mark.asyncio
    async def test_properties(self) -> None:
        """Test the properties flow."""

        # 1. List properties
        properties = await self.adapter.list_properties()
        assert properties is not None
        assert isinstance(properties, PropertyList)
        assert isinstance(properties.items, list)
        properties_count = properties.count
        assert properties_count >= 0

        # 2. Get property details for the first property if it exists
        if properties_count > 0:
            # 2.1. Get property details
            first_property_id = properties.items[0].id
            property_details = await self.adapter.get_property(property_id=first_property_id)
            assert property_details is not None
            assert isinstance(property_details, Property)
            assert property_details.id == first_property_id

        # 3. Create a new property with a unique ID and then delete it to clean up
        property_id = "BUD"
        payload = CreateProperty(
            code=property_id,
            name={
                "en": "Test Property Budapest",
                "de": "Test Immobilie Budapest",
                "it": "Test Proprietà Budapest",
            },
            company_name="Test Company Budapest",
            commercial_register_entry="Test Commercial Register Entry Budapest",
            tax_id="Test Tax ID Budapest",
            location=CreateAddress(
                address_line1="Test Street 1",
                postal_code="1015",
                city="Budapest",
                country_code="AT",
            ),
            time_zone="Europe/Budapest",
            default_check_in_time="15:00:00",
            default_check_out_time="11:00:00",
            currency_code="HUF",
            payment_terms={
                "en": "Test Payment Terms Budapest",
                "de": "Test Zahlungsbedingungen Budapest",
            },
        )
        _ = await self.adapter.create_property(payload=payload, idempotency_key=property_id)

        # property_created = await self.adapter.update_property(
        #     property_id=first_property_id,
        #     payload=[
        #         Operation(
        #             op="test",
        #             path="/city",
        #             value="Berlin-1",
        #         ),
        #         Operation(
        #             op="test",
        #             path="/postal_code",
        #             value="10117-1",
        #         ),
        #     ],
        # )

    @pytest.mark.asyncio
    async def test_is_property(self) -> None:
        """Test checking if a property exists."""
        is_property_true = await self.adapter.is_property(property_id="BER")
        assert is_property_true is not None
        assert isinstance(is_property_true, bool)
        assert is_property_true is True

        # Test with an invalid property ID to check the False case
        is_property_false = await self.adapter.is_property(property_id="INVALID_PROPERTY_ID")
        assert is_property_false is not None
        assert isinstance(is_property_false, bool)
        assert is_property_false is False
