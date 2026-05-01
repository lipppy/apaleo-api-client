import asyncio
from dataclasses import asdict, is_dataclass
from typing import Any, Type, cast

from dacite import from_dict
from pydantic import ValidationError
from pydantic_core import PydanticSerializationError

from apaleoapi.apaleo.common.contracts.factory import CountFakerFactory
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.contracts.response import Count
from apaleoapi.apaleo.common.schemas.factory import CountModelDefaultFactory
from apaleoapi.apaleo.common.schemas.payload import OperationModel
from apaleoapi.apaleo.common.schemas.response import CountModel
from apaleoapi.exceptions import (
    APIError,
    ParameterSerializationError,
    PayloadSerializationError,
    UpdateResourceError,
)
from apaleoapi.logging import get_logger
from apaleoapi.ports.http.transport import AsyncTransportPort
from apaleoapi.services.response_handler import ResponseHandler
from apaleoapi.services.response_validator import ResponseValidator
from apaleoapi.services.url_path_validator import URLPathValidator
from apaleoapi.typing import (
    TBatchModel,
    TDomain,
    TDomainFactory,
    TListModel,
    TModel,
    TModelFactory,
    TParams,
    TParamsModel,
    TPayload,
    TPayloadModel,
)

log = get_logger(__name__)


class BaseAdapter:
    def __init__(
        self, transport: AsyncTransportPort, max_concurrent: int, dry_run: bool = False
    ) -> None:
        self._t = transport
        self._max_concurrent = max_concurrent
        self._dry_run = dry_run
        self._response_handler = ResponseHandler()
        self._response_validator = ResponseValidator()
        self._url_path_validator = URLPathValidator()

    async def _serialize_params(
        self, params: TParams | dict[str, Any] | None, params_model_cls: Type[TParamsModel] | None
    ) -> dict[str, Any]:
        """Helper to validate and serialize query parameters."""
        if is_dataclass(params):
            params_dict = asdict(params)
        elif isinstance(params, dict):
            params_dict = params
        else:
            params_dict = {}
        try:
            params_model = (
                params_model_cls.model_validate(params_dict) if params_model_cls else None
            )
        except ValidationError as e:
            log.error(f"Failed to validate params: {e}")
            raise ParameterSerializationError(
                f"Failed to validate query parameters: {e}",
            ) from e
        try:
            serialized_params = (
                params_model.model_dump(by_alias=True, exclude_none=True) if params_model else {}
            )
        except PydanticSerializationError as e:
            log.error(f"Failed to serialize params: {e}")
            raise ParameterSerializationError(
                f"Failed to serialize query parameters: {e}",
            ) from e
        return serialized_params

    async def _serialize_payload(
        self,
        payload: TPayload | dict[str, Any],
        payload_model_cls: Type[TPayloadModel],
    ) -> dict[str, Any]:
        """Helper to validate and serialize payload data."""
        if is_dataclass(payload):
            payload_dict = asdict(payload)
        elif isinstance(payload, dict):
            payload_dict = payload
        else:
            raise PayloadSerializationError("Payload must be a dataclass instance or a dictionary.")
        try:
            payload_model = payload_model_cls.model_validate(payload_dict)
        except ValidationError as e:
            log.error(f"Failed to validate payload: {e}")
            raise PayloadSerializationError(
                f"Failed to validate payload: {e}",
            ) from e
        try:
            serialized_payload = payload_model.model_dump(by_alias=True) if payload_model else {}
        except PydanticSerializationError as e:
            log.error(f"Failed to serialize payload: {e}")
            raise PayloadSerializationError(
                f"Failed to serialize payload: {e}",
            ) from e
        return serialized_payload

    async def _serialize_patch_payload(
        self,
        payload: list[Operation] | list[dict[str, Any]],
        payload_model_cls: Type[TPayloadModel],
    ) -> list[dict[str, Any]]:
        """Helper to validate and serialize patch payload data."""
        serialized_payloads: list[dict[str, Any]] = []
        for operation in payload:
            if is_dataclass(operation):
                payload_dict = asdict(operation)
            elif isinstance(operation, dict):
                payload_dict = operation
            else:
                raise PayloadSerializationError(
                    "Each item in the payload list must be a dataclass instance or a dictionary."
                )
            try:
                payload_model = payload_model_cls.model_validate(payload_dict)
            except ValidationError as e:
                log.error(f"Failed to validate payload item: {e}")
                raise PayloadSerializationError(
                    f"Failed to validate payload item: {e}",
                ) from e
            try:
                payload_request = (
                    payload_model.model_dump(by_alias=True, exclude_none=True)
                    if payload_model
                    else {}
                )
            except PydanticSerializationError as e:
                log.error(f"Failed to serialize payload item: {e}")
                raise PayloadSerializationError(
                    f"Failed to serialize payload item: {e}",
                ) from e
            serialized_payloads.append(payload_request)
        return serialized_payloads

    async def _head_resource(
        self,
        url: str,
        *,
        error_prefix: str,
    ) -> bool:
        """
        Helper for HEAD requests to check resource existence.
        Returns True if resource exists, False if not found.
        Raises APIError for unexpected response status codes.
        """

        success_codes = {200}

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        # Handle dry run by returning fake data without making an actual API call
        if self._dry_run:
            return True

        # Make the API request and handle the response
        response = await self._t.request(
            "HEAD",
            validated_url,
        )

        # Validate the response data, handling empty responses for success codes
        if response.status_code in success_codes:
            return True
        elif response.status_code == 404:
            return False
        else:
            # Normally no response data is expected for a HEAD request
            _ = self._response_handler.handle(response=response)
            # If no error was raised until this point, a generic APIError is raised to indicate
            # an unexpected response status code.
            raise APIError(
                f"{error_prefix}: Unexpected response for HEAD request to {validated_url}.",
                response=response,
            )

    async def _get_resource(
        self,
        url: str,
        params: TParams | dict[str, Any] | None = None,
        *,
        params_model_cls: Type[TParamsModel] | None = None,
        model_cls: Type[TModel],
        faker_factory: Type[TDomainFactory],
        default_factory: Type[TModelFactory],
        return_cls: Type[TDomain],
        success_codes: set[int],
        error_prefix: str,
        empty_log_message: str = "No item(s) found.",
    ) -> TDomain:
        """Helper for GET item or list resources without batching or concurrency."""

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        # Validate and serialize params if provided, otherwise use empty dict
        params_request = await self._serialize_params(
            params=params, params_model_cls=params_model_cls
        )

        # Handle dry run by returning fake data without making an actual API call
        if self._dry_run:
            fake_response = faker_factory().build()
            return cast(TDomain, fake_response)

        # Make the API request and handle the response
        response = await self._t.request(
            "GET",
            validated_url,
            params=params_request,
        )
        response_data = self._response_handler.handle(response=response)

        # Validate the response data, handling empty responses for success codes
        if response_data is None and response.status_code in success_codes:
            if empty_log_message:
                log.debug(empty_log_message)
            validated_response = default_factory.build()
        else:
            validated_response = self._response_validator.validate(
                response_data=response_data,
                response=response,
                model_cls=model_cls,
                error_prefix=error_prefix,
            )

        data = validated_response.model_dump()
        # Calculate count for list responses if not provided by the API
        # based on the number of items returned
        if "count" in data and "items" in data and isinstance(data["items"], list):
            data["count"] = len(data["items"])
            log.debug(
                f"Calculated count based on items length for class {return_cls.__name__}: "
                f"{data['count']}"
            )

        # Convert the validated response model to the desired return type using from_dict
        return from_dict(
            data_class=return_cls,
            data=data,
        )

    async def _get_resource_count(
        self,
        url: str,
        params: TParams | dict[str, Any] | None = None,
        params_model_cls: Type[TParamsModel] | None = None,
        *,
        error_prefix: str,
    ) -> int:
        """Helper for GET count of resources."""

        count_entity = await self._get_resource(
            url=url,
            params=params,
            params_model_cls=params_model_cls,
            model_cls=CountModel,
            faker_factory=CountFakerFactory,
            default_factory=CountModelDefaultFactory,
            return_cls=Count,
            success_codes={200},
            error_prefix=error_prefix,
            empty_log_message="Count returned no data, defaulting to 0.",
        )
        return count_entity.count

    async def _get_resource_concurrently(
        self,
        url: str,
        params: TParams | dict[str, Any] | None = None,
        *,
        params_model_cls: Type[TBatchModel] | None = None,
        model_cls: Type[TListModel],
        faker_factory: Type[TDomainFactory],
        default_factory: Type[TModelFactory],
        return_cls: Type[TDomain],
        success_codes: set[int],
        error_prefix: str,
        empty_log_message: str = "No items found.",
    ) -> TDomain:
        """Helper for GET list resources with batching and concurrency."""

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        # Limit concurrent requests to avoid overwhelming the API
        semaphore = asyncio.Semaphore(self._max_concurrent)  # Allow max concurrent requests
        all_models: list[TListModel] = []

        async def _fetch_data(params: TBatchModel | None) -> TListModel:
            params_dict = params.model_dump(by_alias=True, exclude_none=True) if params else {}
            response = await self._t.request("GET", validated_url, params=params_dict)
            response_data = self._response_handler.handle(response)
            # Validate the response data, handling empty responses for success codes
            if response_data is None and response.status_code in success_codes:
                if empty_log_message:
                    log.debug(empty_log_message)
                validated_response = cast(TListModel, default_factory.build())
            else:
                validated_response = self._response_validator.validate(
                    response_data=response_data,
                    response=response,
                    model_cls=model_cls,
                    error_prefix=error_prefix,
                )
            return validated_response

        async def _fetch_single(params: TBatchModel) -> TListModel:
            """Fetch a single page to get the total count."""
            single_params = params.model_copy()
            single_params.page_number = 1
            single_params.page_size = 1
            result = await _fetch_data(single_params)
            log.info(f"Fetched page {single_params.page_number} with {len(result.items)} items.")
            return result

        async def _fetch_with_semaphore(params: TBatchModel) -> TListModel:
            """Fetch a page with semaphore to limit concurrency."""
            async with semaphore:
                return await _fetch_data(params)

        # Validate and serialize params if provided, otherwise use empty dict
        params_dict: dict[str, Any] = asdict(params) if is_dataclass(params) else {}
        params_model = params_model_cls.model_validate(params_dict) if params_model_cls else None

        # Handle dry run by returning fake data without making an actual API call
        if self._dry_run:
            fake_response = faker_factory().build()
            return cast(TDomain, fake_response)

        if (
            params_model is not None
            and params_model.batch_size is not None
            and params_model.batch_size > 0
            and params_model.is_concurrently
        ):
            # Fetch all pages concurrently
            single_result = await _fetch_single(params_model)
            object_count = single_result.count
            log.info(f"Total count to fetch: {object_count}")
            total_count = 0
            page_number = 1
            page_size = params_model.batch_size
            pages = (object_count + page_size - 1) // page_size
            # Create tasks for all pages
            tasks: list[asyncio.Task[TListModel]] = []
            for page_number in range(1, pages + 1):
                paginated_params = params_model.model_copy()
                paginated_params.page_number = page_number
                paginated_params.page_size = page_size
                task: asyncio.Task[TListModel] = asyncio.create_task(
                    _fetch_with_semaphore(paginated_params)
                )
                tasks.append(task)
            pages_data: list[TListModel] = await asyncio.gather(*tasks)

            for page in pages_data:
                if page is not None:
                    all_models.append(page)
            # Merge all models into a single model
            merged_models = model_cls(
                items=[item for page in all_models for item in page.items],
                count=sum(len(page.items) for page in all_models),
            )
            validated_response = merged_models
        elif (
            params_model is not None and (batch_size := params_model.batch_size) and batch_size > 0
        ):
            # Fetch all pages sequentially with batch size
            total_count = 0
            page_number = 1
            page_size = batch_size
            while True:
                paginated_params = params_model.model_copy()
                paginated_params.page_number = page_number
                paginated_params.page_size = page_size
                log.info(f"Fetching page {page_number} with batch size {page_size}...")
                result = await _fetch_data(params=paginated_params)
                all_models.append(result)
                total_count += len(result.items)
                log.info(f"Total fetched: {total_count}/{result.count}")
                if total_count >= result.count or result.items == []:
                    break
                page_number += 1

            # Merge all models into a single model
            merged_models = model_cls(
                items=[item for page in all_models for item in page.items],
                count=sum(len(page.items) for page in all_models),
            )

            validated_response = merged_models
        else:
            # Otherwise, fetch all items in a single request
            validated_response = await _fetch_data(params=params_model)

        # Convert the validated response model to the desired return type using from_dict
        return from_dict(
            data_class=return_cls,
            data=validated_response.model_dump(),
        )

    async def _post_resource(
        self,
        url: str,
        payload: TPayload | dict[str, Any],
        idempotency_key: str | None = None,
        *,
        payload_model_cls: Type[TPayloadModel],
        model_cls: Type[TModel],
        faker_factory: Type[TDomainFactory],
        default_factory: Type[TModelFactory],
        return_cls: Type[TDomain],
        success_codes: set[int],
        error_prefix: str,
        empty_log_message: str = "No item(s) found.",
    ) -> TDomain:
        """
        Helper for POST resources.

        Handles dry run by logging and skipping the actual API call.
        Raises exceptions for error responses and logs warnings for unexpected responses.
        """

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        # Validate and serialize payload
        payload_request = await self._serialize_payload(payload, payload_model_cls)

        # In dry run mode we do not skip the validation and serialization of the payload,
        # to ensure that the payload is valid and can be serialized correctly.
        if self._dry_run:
            fake_response = faker_factory().build()
            return cast(TDomain, fake_response)

        # Idempotency key handling for POST requests to prevent duplicate resource creation
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        # Make the API request and handle the response
        response = await self._t.request(
            "POST", validated_url, json=payload_request, headers=headers
        )
        response_data = self._response_handler.handle(response=response)

        # Validate the response data, handling empty responses for success codes
        if response_data is None and response.status_code in success_codes:
            if empty_log_message:
                log.debug(empty_log_message)
            validated_response = default_factory.build()
        else:
            validated_response = self._response_validator.validate(
                response_data=response_data,
                response=response,
                model_cls=model_cls,
                error_prefix=error_prefix,
            )

        # Convert the validated response model to the desired return type using from_dict
        return from_dict(
            data_class=return_cls,
            data=validated_response.model_dump(),
        )

    async def _patch_resource(
        self,
        url: str,
        payload: list[Operation] | list[dict[str, Any]],
        payload_model_cls: Type[OperationModel] = OperationModel,
        *,
        error_prefix: str,
    ) -> None:
        """
        Helper for PATCH resources.

        Handles dry run by logging and skipping the actual API call.
        Raises exceptions for error responses and logs warnings for unexpected responses.
        """
        success_codes = {204}

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        # Validate and serialize patch payload
        serialized_payload = await self._serialize_patch_payload(payload, payload_model_cls)

        # In dry run mode we do not skip the validation and serialization of the payload,
        # to ensure that the payload is valid and can be serialized correctly.
        if self._dry_run:
            return None

        response = await self._t.request("PATCH", validated_url, json=serialized_payload)
        response_data = self._response_handler.handle(response=response)

        # No response data is expected for a successful PATCH
        if response.status_code in success_codes and response_data is None:
            return None

        log.warning(f"PATCH request to {validated_url} returned unexpected data: {response_data}")
        raise UpdateResourceError(
            f"{error_prefix}: Unexpected response data for PATCH request.",
            response,
        )

    async def _delete_resource(self, url: str) -> None:
        """
        Helper for DELETE resources.

        Handles dry run by logging and skipping the actual API call.
        Raises exceptions for error responses and logs warnings for unexpected responses.
        """

        # Validate URL path to prevent injection and ensure it conforms to expected patterns
        validated_url = self._url_path_validator.validate(url)

        if self._dry_run:
            log.info(f"Dry run enabled - skipping DELETE request to {validated_url}")
            return None

        response = await self._t.request("DELETE", validated_url)
        response_data = self._response_handler.handle(response)
        # If nor error was raised, we consider the deletion successful,
        # even if the response is not empty or does not have the expected status code.
        if response_data is not None:
            log.warning(
                f"DELETE request to {validated_url} returned unexpected data: {response_data}"
            )
        if response.status_code != 204:
            log.warning(
                f"DELETE request to {validated_url} returned unexpected status "
                f"code: {response.status_code}"
            )

        return None
