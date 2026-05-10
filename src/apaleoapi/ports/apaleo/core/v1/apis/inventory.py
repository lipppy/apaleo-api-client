"""
Apaleo Core V1 Inventory API Port

See: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from typing import Any, Protocol

from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.core.v1.contracts.inventory.payload import CreateProperty
from apaleoapi.apaleo.core.v1.contracts.inventory.query import (
    PropertyGetParams,
    PropertyListParams,
)
from apaleoapi.apaleo.core.v1.contracts.inventory.response import (
    CountryList,
    Property,
    PropertyList,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.response import PropertyCreated


class CoreV1InventoryResourcePort(Protocol):
    _path: str = "inventory"
    _version: str

    # Property methods

    async def list_properties(
        self, params: PropertyListParams | dict[str, Any] | None = None
    ) -> PropertyList:
        """List properties with optional filters."""
        pass

    async def create_property(
        self, payload: CreateProperty | dict[str, Any], idempotency_key: str | None = None
    ) -> PropertyCreated:
        """Create a new property."""
        pass

    async def count_properties(self) -> int:
        """Get total count of properties."""
        pass

    async def get_property(
        self, property_id: str, params: PropertyGetParams | dict[str, Any] | None = None
    ) -> Property:
        """Get property details by ID."""
        pass

    async def update_property(
        self, property_id: str, payload: list[Operation] | list[dict[str, Any]]
    ) -> None:
        """Update property details by ID."""
        pass

    async def delete_property(self, property_id: str) -> None:
        """Delete property by ID."""
        pass

    # Property Actions methods

    async def clone_property(
        self,
        property_id: str,
        payload: CreateProperty | dict[str, Any],
        idempotency_key: str | None = None,
    ) -> PropertyCreated:
        """Clone a property by ID."""
        pass

    async def archive_property(self, property_id: str) -> None:
        """Archive a live property by ID."""
        pass

    async def activate_property(self, property_id: str) -> None:
        """Set a test property live by ID."""
        pass

    async def reset_property(self, property_id: str) -> None:
        """Reset a test property by ID."""
        pass

    # Types methods

    async def list_countries(self) -> CountryList:
        """List available countries."""
        pass

    # Unit methods

    # Unit Actions methods

    # Unit Attribute methods

    # Unit Group methods
