from polyfactory.factories.pydantic_factory import ModelFactory

from apaleoapi.apaleo.core.v1.schemas.inventory.response import (
    CountryListModel,
    PropertyListModel,
    PropertyModel,
)
from apaleoapi.apaleo.identity.v1.schemas.identity.response import PropertyCreatedModel


class CountryListModelDefaultFactory(ModelFactory[CountryListModel]):
    __model__ = CountryListModel
    __use_defaults__ = True


class PropertyCreatedModelDefaultFactory(ModelFactory[PropertyCreatedModel]):
    __model__ = PropertyCreatedModel
    __use_defaults__ = True


class PropertyListModelDefaultFactory(ModelFactory[PropertyListModel]):
    __model__ = PropertyListModel
    __use_defaults__ = True


class PropertyModelDefaultFactory(ModelFactory[PropertyModel]):
    __model__ = PropertyModel
    __use_defaults__ = True
