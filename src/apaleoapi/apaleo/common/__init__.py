"""Apaleo API - Common.

Centralized module for common functionality with convenient imports
for all dataclasses, enums, and parameters.

Usage:
    # Import specific entities
    from apaleoapi.apaleo.common import Count, Operation

    # Or import from sub-modules for organization
    from apaleoapi.apaleo.common.contracts.payload import Operation
    from apaleoapi.apaleo.common.contracts.response import Count
"""

from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.contracts.response import Count

__all__ = [
    # Dataclasses - Response
    "Count",
    # Dataclasses - Payload
    "Operation",
]
