"""Apaleo Core API - Inventory V1.

Centralized module for Inventory V1 with convenient imports
for all dataclasses, enums, and parameters.

Usage:
    # Import specific entities
    from apaleoapi.apaleo.core.v1.inventory import Property, PropertyList, PropertyStatus

    # Or import from sub-modules for organization
    from apaleoapi.apaleo.core.v1.contracts.inventory.response import Property
    from apaleoapi.apaleo.core.v1.enums.inventory import PropertyStatus
"""

from apaleoapi.apaleo.core.v1.contracts.inventory.common import Address, BankAccount
from apaleoapi.apaleo.core.v1.contracts.inventory.factory import (
    CountryListFakerFactory,
    PropertyCreatedFakerFactory,
    PropertyFakerFactory,
    PropertyListFakerFactory,
)
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
from apaleoapi.apaleo.core.v1.enums.inventory import (
    PropertyStatus,
)
from apaleoapi.apaleo.identity.v1.contracts.identity.response import PropertyCreated

__all__ = [
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
    # Factories
    "CountryListFakerFactory",
    "PropertyCreatedFakerFactory",
    "PropertyListFakerFactory",
    "PropertyFakerFactory",
    # Enums
    "PropertyAction",
    "PropertyActionCode",
    "PropertyStatus",
]
