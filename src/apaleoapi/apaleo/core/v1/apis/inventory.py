"""
Apaleo Core V1 Inventory API Adapter

See: https://api.apaleo.com/swagger/index.html?urls.primaryName=Inventory+V1
"""

from dataclasses import asdict, is_dataclass
from typing import Any

from dacite import from_dict

from apaleoapi.apaleo.common.base import BaseAdapter
from apaleoapi.apaleo.core.v1.dataclasses.inventory.query import (
    PropertyGetParams,
    PropertyListParams,
)
from apaleoapi.apaleo.core.v1.dataclasses.inventory.response import (
    CountryList,
    Property,
    PropertyFactory,
    PropertyList,
    PropertyListFakerFactory,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.query import (
    PropertyGetParamsModel,
    PropertyListParamsModel,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.response import (
    CountryListModel,
    PropertyListModel,
    PropertyListModelDefaultFactory,
    PropertyModel,
)
from apaleoapi.logging import get_logger
from apaleoapi.ports.apaleo.core.v1.apis.inventory import CoreV1InventoryResourcePort
from apaleoapi.ports.http.transport import AsyncTransportPort

log = get_logger(__name__)


class CoreV1InventoryAdapter(BaseAdapter, CoreV1InventoryResourcePort):
    def __init__(self, transport: AsyncTransportPort, max_concurrent: int, dry_run: bool = False):
        super().__init__(transport=transport, max_concurrent=max_concurrent, dry_run=dry_run)
        self._version = "v1"
        self._base_path = f"{self._path}/{self._version}"

    # Property methods

    async def list_properties(self, params: PropertyListParams | None = None) -> PropertyList:
        """
        List properties with optional filters.

        Args:
            params (PropertyListParams, optional):
                Filters and pagination options for listing properties.

                Supported fields:
                    - status (str):
                        Filter properties by status. Allowed values: "Test", "Live".

                    - include_archived (bool):
                        Whether to include archived properties in the results.
                        If omitted or False, only non-archived properties are returned.

                    - country_code (str):
                        Filter properties by ISO country code (e.g., "US", "DE").

                    - expand (list[str]):
                        List of embedded resources to expand in the response.
                        Supported values: "actions". All other values are ignored.

                    - page_number (int):
                        Page number to retrieve. Default: 1.
                        If the requested page contains no items, the API returns
                        HTTP 204 (No Content).

                    - page_size (int):
                        Number of items per page. Default: 500. Maximum: 500.

                    - batch_size (int):
                        Number of items fetched per request when retrieving pages
                        concurrently.

                    - is_concurrently (bool):
                        Whether pages should be fetched concurrently. Default: False.

        Returns:
            PropertyList:
                A list of properties matching the provided filters.
        """
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

    async def create_property(self, idempotency_key: str) -> Any:
        raise NotImplementedError("Create property method is not implemented yet.")

    async def count_properties(self) -> int:
        """Get total count of properties."""
        url = f"{self._base_path}/properties/$count"

        return await self._get_resource_count(
            url=url,
            error_prefix="Failed to count properties",
        )

    async def _get_property(
        self, property_id: str, params: PropertyGetParamsModel
    ) -> PropertyModel:
        """Helper method to get property details by ID, returning validated response model."""
        url = f"{self._base_path}/properties/{property_id}"
        params_dict = params.model_dump(by_alias=True, exclude_none=True)
        response = await self._t.request("GET", url, params=params_dict)
        response_data = self._response_handler.handle(response)
        return self._response_validator.validate(
            response_data=response_data,
            response=response,
            model_cls=PropertyModel,
            error_prefix="Invalid property item payload from Apaleo inventory",
        )

    async def get_property(
        self, property_id: str, params: PropertyGetParams | None = None
    ) -> Property:
        """Get property details by ID."""
        params_dict: dict[str, Any] = asdict(params) if is_dataclass(params) else {}
        params_model = PropertyGetParamsModel.model_validate(params_dict)
        if self._dry_run:
            fake_response = PropertyFactory().build()
            return fake_response
        validated_response = await self._get_property(property_id=property_id, params=params_model)
        return from_dict(data_class=Property, data=validated_response.model_dump())

    # Types methods

    async def _list_countries(self) -> CountryListModel:
        """
        Helper method to list available countries, returning validated response model.
        """
        url = f"{self._base_path}/types/countries"
        response = await self._t.request("GET", url)
        response_data = self._response_handler.handle(response)
        return self._response_validator.validate(
            response_data=response_data,
            response=response,
            model_cls=CountryListModel,
            error_prefix="Invalid country list payload from Apaleo inventory",
        )

    async def list_countries(self) -> CountryList:
        """
        List available countries.
        """
        validated_response = await self._list_countries()
        return from_dict(data_class=CountryList, data=validated_response.model_dump())
