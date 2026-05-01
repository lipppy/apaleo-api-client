import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING or sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum


class OperationOp(StrEnum):
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"
