from dataclasses import dataclass

from apaleoapi.dataclasses import BatchRequest


@dataclass
class PropertyListParams(BatchRequest):
    status: list[str] | None = None
    include_archived: bool | None = None
    country_code: list[str] | None = None
    expand: list[str] | None = None


@dataclass
class PropertyGetParams:
    languages: list[str] | None = None
    expand: list[str] | None = None
