from dataclasses import dataclass


@dataclass
class BatchRequest:
    page_number: int | None = None
    page_size: int | None = None
    batch_size: int | None = None
    is_concurrently: bool | None = None
