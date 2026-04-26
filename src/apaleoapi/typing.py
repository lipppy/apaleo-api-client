from typing import TYPE_CHECKING, Any, TypeVar

from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from apaleoapi.apaleo.common.schemas.base import BatchRequestBaseModel, ListBaseModel

if TYPE_CHECKING:
    from _typeshed import DataclassInstance
else:
    DataclassInstance = Any


TDomain = TypeVar("TDomain", bound=DataclassInstance)
TParams = TypeVar("TParams", bound=DataclassInstance)
TPayload = TypeVar("TPayload", bound=DataclassInstance)
TModel = TypeVar("TModel", bound=BaseModel)
TParamsModel = TypeVar("TParamsModel", bound=BaseModel)
TPayloadModel = TypeVar("TPayloadModel", bound=BaseModel)
TBatchModel = TypeVar("TBatchModel", bound=BatchRequestBaseModel)
TListModel = TypeVar("TListModel", bound=ListBaseModel[Any])

TDomainFactory = TypeVar("TDomainFactory", bound=DataclassFactory[Any])
TParamsFactory = TypeVar("TParamsFactory", bound=DataclassFactory[Any])
TPayloadFactory = TypeVar("TPayloadFactory", bound=DataclassFactory[Any])
TModelFactory = TypeVar("TModelFactory", bound=ModelFactory[Any])
