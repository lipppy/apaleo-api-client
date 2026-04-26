from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Operation:
    value: Any | None = None
    path: str | None = None
    op: str | None = None
    from_: str | None = None
