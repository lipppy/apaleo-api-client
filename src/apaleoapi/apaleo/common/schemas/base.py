from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

TModel = TypeVar("TModel", bound=BaseModel)
TEnum = TypeVar("TEnum", bound=Any)


class ExtendedBaseModel(BaseModel):
    """Common base model with extended Pydantic configuration."""

    model_config = {
        "populate_by_name": True,  # Enable population by field name
    }


class StrictBaseModel(BaseModel):
    """Common base model with strict Pydantic configuration."""

    model_config = {
        "populate_by_name": True,  # Enable population by field name
        "extra": "forbid",  # Forbid extra fields not defined in the model
    }


class ImmutableBaseModel(BaseModel):
    """Common base model with immutable Pydantic configuration."""

    model_config = {
        "populate_by_name": True,  # Enable population by field name
        "frozen": True,  # Make the model immutable
    }


class BatchRequestBaseModel(StrictBaseModel):
    """Base model for batch requests."""

    page_number: Optional[int] = Field(None, alias="pageNumber")
    page_size: Optional[int] = Field(None, alias="pageSize", gt=0)
    batch_size: Optional[int] = Field(
        None, alias="batchSize", gt=0
    )  # Optional batch size for batch requests
    is_concurrently: Optional[bool] = Field(
        None, alias="isConcurrently"
    )  # Flag to indicate concurrent fetching


class ListBaseModel(ExtendedBaseModel, Generic[TModel]):
    """Base model for list responses."""

    items: list[TModel] = Field(default_factory=list)  # Default to empty list for items
    count: int = Field(default=0, description="Total number of items in the list.")


class ListStringBaseModel(ExtendedBaseModel):
    """Base model for list responses."""

    items: list[str] = Field(default_factory=list)  # Default to empty list for items
    count: int = Field(default=0, description="Total number of items in the list.")


class ListEnumBaseModel(ExtendedBaseModel, Generic[TEnum]):
    """Base model for list responses."""

    items: list[TEnum] = Field(default_factory=list)  # Default to empty list for items
    count: int = Field(default=0, description="Total number of items in the list.")
