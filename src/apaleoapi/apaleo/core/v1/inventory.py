"""Apaleo Core API - Inventory V1.

Centralized module for Inventory V1 with convenient imports
for all dataclasses, enums, and parameters.

Usage:
    # Import specific entities
    from apaleoapi.apaleo.core.v1.inventory import Property, PropertyList

    # Or import from sub-modules for organization
    from apaleoapi.apaleo.core.v1.contracts.inventory.response import Property
    from apaleoapi.apaleo.core.v1.enums.inventory import Status
"""

from apaleoapi.apaleo.core.v1.contracts.inventory.common import Address, BankAccount
from apaleoapi.apaleo.core.v1.contracts.inventory.payload import (
    CreateAddress,
    CreateProperty,
)
from apaleoapi.apaleo.core.v1.contracts.inventory.query import (
    PropertyGetParams,
    PropertyListParams,
)
from apaleoapi.apaleo.core.v1.contracts.inventory.response import (
    Action,
    ActionReason,
    CountryList,
    Property,
    PropertyItem,
    PropertyList,
)
from apaleoapi.apaleo.core.v1.enums.inventory import Action as PropertyAction
from apaleoapi.apaleo.core.v1.enums.inventory import Code as PropertyActionCode
from apaleoapi.apaleo.core.v1.enums.inventory import Status as PropertyStatus
from apaleoapi.apaleo.core.v1.factories.inventory import (
    CountryListModelDefaultFactory,
    CountryListModelFakerFactory,
    PropertyCreatedModelDefaultFactory,
    PropertyCreatedModelFakerFactory,
    PropertyListModelDefaultFactory,
    PropertyListModelFakerFactory,
    PropertyModelDefaultFactory,
    PropertyModelFakerFactory,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.common import BankAccountModel
from apaleoapi.apaleo.core.v1.schemas.inventory.payload import (
    CreateAddressModel,
    CreatePropertyModel,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.query import (
    PropertyGetParamsModel,
    PropertyListParamsModel,
)
from apaleoapi.apaleo.core.v1.schemas.inventory.response import (
    ActionModel,
    ActionReasonModel,
    AddressModel,
    CountryListModel,
    PropertyCreatedModel,
    PropertyItemModel,
    PropertyListModel,
    PropertyModel,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.response import PropertyCreated

__all__ = [
    # Enums
    "PropertyAction",
    "PropertyActionCode",
    "PropertyStatus",
    # Dataclasses - Common
    "Address",
    "BankAccount",
    # Dataclasses - Response
    "Action",
    "ActionReason",
    "CountryList",
    "Property",
    "PropertyCreated",
    "PropertyItem",
    "PropertyList",
    # Dataclasses - Payload
    "CreateAddress",
    "CreateProperty",
    # Dataclasses - Query Parameters
    "PropertyGetParams",
    "PropertyListParams",
    # Schemas - Common
    "AddressModel",
    "BankAccountModel",
    # Schemas - Response
    "ActionReasonModel",
    "ActionModel",
    "CountryListModel",
    "PropertyCreatedModel",
    "PropertyItemModel",
    "PropertyListModel",
    "PropertyModel",
    # Schemas - Payload
    "CreateAddressModel",
    "CreatePropertyModel",
    # Schemas - Query Parameters
    "PropertyGetParamsModel",
    "PropertyListParamsModel",
    # Factories
    "CountryListModelFakerFactory",
    "PropertyCreatedModelFakerFactory",
    "PropertyListModelFakerFactory",
    "PropertyModelFakerFactory",
    "CountryListModelDefaultFactory",
    "PropertyCreatedModelDefaultFactory",
    "PropertyListModelDefaultFactory",
    "PropertyModelDefaultFactory",
]
