from dataclasses import dataclass
from typing import Any

from apaleoapi.apaleo.common.enums import OperationOp


@dataclass(frozen=True)
class Operation:
    """
    Represents a single JSON Patch operation as defined in RFC 6902.

        - op: The operation type (add, remove, replace, move, copy, test).
            - add: Adds a new field or array element.
            - remove: Deletes a field.
            - replace: Updates an existing field.
            - move: Moves a value to a different location.
            - copy: Copies a value to a new location.
            - test: Verifies a value before applying operations.
        - path: The JSON Pointer path to the target location.
        - value: The value to be used within the operation.
        - from_: The source path for move and copy operations.
    """

    value: Any | None = None
    path: str | None = None
    op: OperationOp | None = None
    from_: str | None = None
