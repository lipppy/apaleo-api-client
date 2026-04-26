from polyfactory.factories.pydantic_factory import ModelFactory

from apaleoapi.apaleo.common.schemas.payload import OperationModel
from apaleoapi.apaleo.common.schemas.response import CountModel


class CountModelDefaultFactory(ModelFactory[CountModel]):
    __model__ = CountModel
    __use_defaults__ = True


class OperationModelDefaultFactory(ModelFactory[OperationModel]):
    __model__ = OperationModel
    __use_defaults__ = True
