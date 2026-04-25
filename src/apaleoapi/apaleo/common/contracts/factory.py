from polyfactory.factories import DataclassFactory

from apaleoapi.apaleo.common.contracts.response import Count


class CountFakerFactory(DataclassFactory[Count]):
    __model__ = Count
