from typing import TYPE_CHECKING, Any, TypeVar

from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from apaleoapi.schemas import BatchRequestBaseModel, ListBaseModel

if TYPE_CHECKING:
    from _typeshed import DataclassInstance
else:
    DataclassInstance = Any

TDomain = TypeVar("TDomain", bound=DataclassInstance)
TDomainFactory = TypeVar("TDomainFactory", bound=DataclassFactory[Any])
TParams = TypeVar("TParams", bound=DataclassInstance)
TParamsFactory = TypeVar("TParamsFactory", bound=DataclassFactory[Any])
TPayload = TypeVar("TPayload", bound=DataclassInstance)
TPayloadFactory = TypeVar("TPayloadFactory", bound=DataclassFactory[Any])
TModel = TypeVar("TModel", bound=BaseModel)
TModelFactory = TypeVar("TModelFactory", bound=ModelFactory[Any])
TBatchModel = TypeVar("TBatchModel", bound=BatchRequestBaseModel)
TListModel = TypeVar("TListModel", bound=ListBaseModel[Any])
