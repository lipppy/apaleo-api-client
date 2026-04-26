from typing import Any, Type

import httpx
from pydantic import ValidationError as PydanticValidationError

from apaleoapi.exceptions import ValidationError
from apaleoapi.logging import get_logger
from apaleoapi.typing import TModel

log = get_logger(__name__)


class ResponseValidator:
    @staticmethod
    def validate(
        *,
        response_data: str | list[Any] | dict[str, Any] | None,
        response: httpx.Response,
        model_cls: Type[TModel],
        error_prefix: str,
    ) -> TModel:
        """
        Validates `response_data` with `model_cls`.

        Raises ValidationError if Pydantic validation fails,
        with message prefixed by `error_prefix`.
        """
        try:
            model = model_cls.model_validate(response_data)
        except PydanticValidationError as e:
            raise ValidationError(f"{error_prefix}: {e}", response) from e
        return model
