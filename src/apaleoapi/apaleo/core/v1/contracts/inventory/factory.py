from polyfactory.factories import DataclassFactory

from apaleoapi.apaleo.core.v1.contracts.inventory.response import Property, PropertyList
from apaleoapi.apaleo.identity.v1.contracts.identity.response import PropertyCreated


class PropertyCreatedFakerFactory(DataclassFactory[PropertyCreated]):
    __model__ = PropertyCreated


class PropertyListFakerFactory(DataclassFactory[PropertyList]):
    __model__ = PropertyList


class PropertyFakerFactory(DataclassFactory[Property]):
    __model__ = Property
