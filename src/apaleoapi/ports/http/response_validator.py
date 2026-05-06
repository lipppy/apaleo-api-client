from typing import Any, Protocol, Type

import httpx

from apaleoapi.typing import TModel


class ResponseValidatorPort(Protocol):
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
        pass
