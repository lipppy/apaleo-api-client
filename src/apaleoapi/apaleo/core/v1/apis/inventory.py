"""
Apaleo Core V1 Inventory API Adapter

See: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from typing import Any

from apaleoapi.apaleo.common.base import BaseAdapter
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.core.v1.contracts.inventory.factory import (
    CountryListFakerFactory,
    PropertyCreatedFakerFactory,
    PropertyFakerFactory,
    PropertyListFakerFactory,
)
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
from apaleoapi.apaleo.core.v1.schemas.inventory.factory import (
    CountryListModelDefaultFactory,
    PropertyCreatedModelDefaultFactory,
    PropertyListModelDefaultFactory,
    PropertyModelDefaultFactory,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.payload import CreatePropertyModel
from apaleoapi.apaleo.core.v1.schemas.inventory.query import (
    PropertyGetParamsModel,
    PropertyListParamsModel,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.response import (
    CountryListModel,
    PropertyCreatedModel,
    PropertyListModel,
    PropertyModel,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.response import PropertyCreated
from apaleoapi.logging import get_logger
from apaleoapi.ports.apaleo.core.v1.apis.inventory import CoreV1InventoryResourcePort
from apaleoapi.ports.http.transport import AsyncTransportPort

log = get_logger(__name__)


class CoreV1InventoryResource(BaseAdapter, CoreV1InventoryResourcePort):
    """Adapter for Core V1 Inventory API endpoints."""

    def __init__(self, transport: AsyncTransportPort, max_concurrent: int, dry_run: bool = False):
        super().__init__(transport=transport, max_concurrent=max_concurrent, dry_run=dry_run)
        self._version = "v1"
        self._base_path = f"{self._path}/{self._version}"

    # Property methods

    async def list_properties(
        self, params: PropertyListParams | dict[str, Any] | None = None
    ) -> PropertyList:
        """List properties with optional filters."""
        url = f"{self._base_path}/properties"

        return await self._get_resource_concurrently(
            url=url,
            params=params,
            params_model_cls=PropertyListParamsModel,
            model_cls=PropertyListModel,
            faker_factory=PropertyListFakerFactory,
            default_factory=PropertyListModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to list properties for the current account",
            return_cls=PropertyList,
        )

    async def create_property(
        self, payload: CreateProperty | dict[str, Any], idempotency_key: str | None = None
    ) -> PropertyCreated:
        """Create a new property."""
        url = f"{self._base_path}/properties"

        return await self._post_resource(
            url=url,
            payload=payload,
            idempotency_key=idempotency_key,
            payload_model_cls=CreatePropertyModel,
            model_cls=PropertyCreatedModel,
            faker_factory=PropertyCreatedFakerFactory,
            default_factory=PropertyCreatedModelDefaultFactory,
            success_codes={200},
            error_prefix="Failed to create a new property",
            return_cls=PropertyCreated,
        )

    async def count_properties(self) -> int:
        """Get total count of properties."""
        url = f"{self._base_path}/properties/$count"

        return await self._get_resource_count(
            url=url,
            error_prefix="Failed to count properties",
        )

    async def check_property(self, property_id: str) -> bool:
        """Check if a property exists by ID."""
        url = f"{self._base_path}/properties/{property_id}"

        return await self._head_resource(
            url=url,
            error_prefix=f"Failed to check existence of property {property_id}",
        )

    async def get_property(
        self, property_id: str, params: PropertyGetParams | dict[str, Any] | None = None
    ) -> Property:
        """Get property details by ID."""
        url = f"{self._base_path}/properties/{property_id}"

        return await self._get_resource(
            url=url,
            params=params,
            params_model_cls=PropertyGetParamsModel,
            model_cls=PropertyModel,
            faker_factory=PropertyFakerFactory,
            default_factory=PropertyModelDefaultFactory,
            success_codes={200, 204},
            error_prefix=f"Failed to get property with ID {property_id}",
            return_cls=Property,
        )

    async def update_property(
        self, property_id: str, payload: list[Operation] | list[dict[str, Any]]
    ) -> None:
        """Update property details by ID."""
        url = f"{self._base_path}/properties/{property_id}"

        return await self._patch_resource(
            url=url,
            payload=payload,
            error_prefix=f"Failed to update property with ID {property_id}",
        )

    async def delete_property(self, property_id: str) -> None:
        """Delete property by ID if it exists."""
        url = f"{self._base_path}/properties/{property_id}"

        await self._delete_resource(url=url)

    # Types methods

    async def list_countries(self) -> CountryList:
        """
        List available countries.
        """
        url = f"{self._base_path}/types/countries"

        return await self._get_resource(
            url=url,
            model_cls=CountryListModel,
            faker_factory=CountryListFakerFactory,
            default_factory=CountryListModelDefaultFactory,
            success_codes={200, 204},
            error_prefix="Failed to list countries",
            return_cls=CountryList,
        )
