import asyncio
from dataclasses import asdict, is_dataclass
from typing import Any, Type, cast

from dacite import from_dict

from apaleoapi.apaleo.common.contracts.factory import CountFakerFactory
from apaleoapi.apaleo.common.contracts.payload import Operation
from apaleoapi.apaleo.common.contracts.response import Count
from apaleoapi.apaleo.common.schemas.factory import CountModelDefaultFactory
from apaleoapi.apaleo.common.schemas.response import CountModel
from apaleoapi.exceptions import UpdateResourceError
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

    async def _get_resource(
        self,
        url: str,
        params: TParams | None = None,
        params_model_cls: Type[TParamsModel] | None = None,
        *,
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
        params_dict: dict[str, Any] = asdict(params) if is_dataclass(params) else {}
        params_model = params_model_cls.model_validate(params_dict) if params_model_cls else None
        params_request = (
            params_model.model_dump(by_alias=True, exclude_none=True) if params_model else {}
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

        # Convert the validated response model to the desired return type using from_dict
        return from_dict(
            data_class=return_cls,
            data=validated_response.model_dump(),
        )

    async def _get_resource_count(
        self,
        url: str,
        params: TParams | None = None,
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
        params: TParams | None = None,
        params_model_cls: Type[TBatchModel] | None = None,
        *,
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
            pages = (object_count // page_size) + 1
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
                log.info(f"Fetching page {page_number} with size {page_size}...")
                result = await _fetch_data(params=paginated_params)
                all_models.append(result)
                total_count += page_size
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
        payload: TPayload,
        payload_model_cls: Type[TModel],
        *,
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
        payload_dict: dict[str, Any] = asdict(payload) if is_dataclass(payload) else {}
        payload_model = (
            payload_model_cls.model_validate(payload_dict) if payload_model_cls else None
        )
        payload_request = (
            payload_model.model_dump(by_alias=True, exclude_none=True) if payload_model else {}
        )

        # In dry run mode we do not skip the validation and serialization of the payload,
        # to ensure that the payload is valid and can be serialized correctly.
        if self._dry_run:
            fake_response = faker_factory().build()
            return cast(TDomain, fake_response)

        response = await self._t.request("POST", validated_url, json=payload_request)
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
        payload: list[Operation],
        payload_model_cls: Type[TPayloadModel],
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

        # Validate and serialize payload
        payload_requests: list[dict[str, Any]] = []
        for operation in payload:
            payload_dict: dict[str, Any] = asdict(operation) if is_dataclass(operation) else {}
            payload_model = (
                payload_model_cls.model_validate(payload_dict) if payload_model_cls else None
            )
            payload_request = (
                payload_model.model_dump(by_alias=True, exclude_none=True) if payload_model else {}
            )
            payload_requests.append(payload_request)
        # In dry run mode we do not skip the validation and serialization of the payload,
        # to ensure that the payload is valid and can be serialized correctly.
        if self._dry_run:
            return None

        response = await self._t.request("PATCH", validated_url, json=payload_requests)
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
