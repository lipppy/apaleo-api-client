"""
Apaleo Core V1 Inventory API Port

See: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from typing import Any, Protocol

from apaleoapi.apaleo.core.v1.dataclasses.inventory.query import (
    PropertyGetParams,
    PropertyListParams,
)
from apaleoapi.apaleo.core.v1.dataclasses.inventory.response import (
    CountryList,
    Property,
    PropertyList,
)


class CoreV1InventoryPort(Protocol):
    _path: str = "inventory"
    _version: str

    # Property methods

    async def list_properties(self, params: PropertyListParams | None = None) -> PropertyList:
        """List properties with optional filters."""
        pass

    async def create_property(self, idempotency_key: str) -> Any:
        """Create a new property."""
        pass

    async def get_property(
        self, property_id: str, params: PropertyGetParams | None = None
    ) -> Property:
        """Get property details by ID."""
        pass

    # Types methods

    async def list_countries(self) -> CountryList:
        """List available countries."""
        pass
