import uuid

import pytest
from dacite import from_dict

from apaleoapi import ApaleoAPIClient
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.enums import OperationOp
from apaleoapi.apaleo.core.v1.apis.inventory import CoreV1InventoryResource
from apaleoapi.apaleo.core.v1.inventory import CreateAddress, CreateProperty, Property, PropertyList

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
        property_id = "INTTEST1"  # Use a unique property ID for testing
        # 3.1 Check if the property already exists to avoid conflicts
        if not await self.adapter.check_property(property_id=property_id):
            # 3.1.1 Create the property
            payload = CreateProperty(
                code=property_id,
                name={
                    "en": "Test Property Budapest",
                    "de": "Test Immobilie Budapest",
                    "it": "Test Proprietà Budapest",
                },
                description={
                    "en": "Test Description Budapest",
                    "de": "Test Beschreibung Budapest",
                    "it": "Test Descrizione Budapest",
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
                    "it": "Test Condizioni di Pagamento Budapest",
                },
            )
            _ = await self.adapter.create_property(
                payload=payload, idempotency_key=str(uuid.uuid4())
            )
            # 3.1.2 Check that the property was created successfully
            property_created = await self.adapter.check_property(property_id=property_id)
            assert property_created is True
            # 3.1.3 List properties again to confirm the count has increased by 1
            properties_after_creation = await self.adapter.list_properties()
            assert properties_after_creation is not None
            assert isinstance(properties_after_creation, PropertyList)
            assert properties_after_creation.count == properties_count + 1
            # 3.1.4 Check with count_properties method to confirm the count is consistent
            properties_count_after_creation = await self.adapter.count_properties()
            assert properties_count_after_creation == properties_count + 1

        # 4. Retrieve the property details again to confirm it can be fetched successfully
        property_details_after_creation = await self.adapter.get_property(property_id=property_id)
        assert property_details_after_creation is not None
        assert isinstance(property_details_after_creation, Property)
        assert property_details_after_creation.id == property_id

        # 5. Update the property details -multiple operations
        description_before_update = property_details_after_creation.description
        description_after_update = (
            description_before_update.copy() if description_before_update else {}
        )
        description_after_update["en"] = "Updated Description"
        await self.adapter.update_property(
            property_id=first_property_id,
            payload=[
                Operation(
                    op=OperationOp.REPLACE,
                    path="/description",
                    value=description_after_update,
                ),
            ],
        )

        # 6. Retrieve the property details again to confirm the updates were applied successfully
        property_details_after_update = await self.adapter.get_property(
            property_id=first_property_id
        )
        assert property_details_after_update is not None
        assert isinstance(property_details_after_update, Property)
        assert property_details_after_update.id == first_property_id
        assert isinstance(property_details_after_update.description, dict)
        assert property_details_after_update.description["en"] == "Updated Description"

        # 7. Clean up by deleting the created property if it was created during the test
        if await self.adapter.check_property(property_id=property_id):
            await self.adapter.delete_property(property_id=property_id)

        # 8. Confirm that the property was deleted successfully
        property_deleted = await self.adapter.check_property(property_id=property_id)
        assert property_deleted is False

    @pytest.mark.asyncio
    async def test_check_property(self) -> None:
        """Test checking if a property exists."""
        check_property_true = await self.adapter.check_property(property_id="BER")
        assert check_property_true is not None
        assert isinstance(check_property_true, bool)
        assert check_property_true is True

        # Test with an invalid property ID to check the False case
        check_property_false = await self.adapter.check_property(property_id="INVALID_PROPERTY_ID")
        assert check_property_false is not None
        assert isinstance(check_property_false, bool)
        assert check_property_false is False

    @pytest.mark.asyncio
    async def test_create_property_from_dict(self) -> None:
        """
        Test creating a property using a dictionary for building the payload.
        The extra tools like dacite are used to convert the dictionary to the model instance.
        """
        property_id = "INTTEST2"  # Use a unique property ID for testing
        # Check if the property already exists to avoid conflicts
        if not await self.adapter.check_property(property_id=property_id):
            payload_dict = {
                "code": property_id,
                "name": {
                    "en": "Test Property Dict",
                    "de": "Test Immobilie Dict",
                    "it": "Test Proprietà Dict",
                },
                "description": {
                    "en": "Test Description Dict",
                    "de": "Test Beschreibung Dict",
                    "it": "Test Descrizione Dict",
                },
                "company_name": "Test Company Dict",
                "commercial_register_entry": "Test Commercial Register Entry Dict",
                "tax_id": "Test Tax ID Dict",
                "location": {
                    "address_line1": "Test Street 1",
                    "postal_code": "1015",
                    "city": "Vienna",
                    "country_code": "AT",
                },
                "time_zone": "Europe/Vienna",
                "default_check_in_time": "15:00:00",
                "default_check_out_time": "11:00:00",
                "currency_code": "EUR",
                "payment_terms": {
                    "en": "Test Payment Terms Dict",
                    "de": "Test Zahlungsbedingungen Dict",
                    "it": "Test Condizioni di Pagamento Dict",
                },
            }
            payload = from_dict(CreateProperty, payload_dict)
            _ = await self.adapter.create_property(
                payload=payload, idempotency_key=str(uuid.uuid4())
            )
            # Clean up by deleting the created property
            if await self.adapter.check_property(property_id=property_id):
                await self.adapter.delete_property(property_id=property_id)
