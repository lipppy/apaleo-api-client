from polyfactory.factories import DataclassFactory

from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.contracts.response import Count


class CountFakerFactory(DataclassFactory[Count]):
    __model__ = Count


class OperationFakerFactory(DataclassFactory[Operation]):
    __model__ = Operation
