import asyncio
from typing import Awaitable, Callable

from apaleoapi.logging import get_logger
from apaleoapi.typing import TBatchModel, TListModel

log = get_logger(__name__)


class ListFetcher:
    """Helper class to fetch data with pagination support."""

    def __init__(self, max_concurrent: int):
        self._max_concurrent = max_concurrent

    async def fetch(
        self,
        fetch_fn: Callable[[TBatchModel], Awaitable[TListModel]],
        params: TBatchModel,
        model_cls: type[TListModel],
        dry_run: bool = False,
    ) -> TListModel:
        """Execute the fetch operation with pagination."""
        # Limit concurrent requests to avoid overwhelming the API
        semaphore = asyncio.Semaphore(self._max_concurrent)  # Allow max concurrent requests
        all_models: list[TListModel] = []

        async def fetch_single(params: TBatchModel) -> TListModel:
            """Fetch a single page to get the total count."""
            single_params = params.model_copy()
            single_params.page_number = 1
            single_params.page_size = 1
            result = await fetch_fn(single_params)
            log.info(f"Fetched page {single_params.page_number} with {len(result.items)} items.")
            return result

        async def fetch_with_semaphore(params: TBatchModel) -> TListModel:
            """Fetch a page with semaphore to limit concurrency."""
            async with semaphore:
                return await fetch_fn(params)

        if dry_run:
            # Return empty model for dry run
            return model_cls()
        elif params.batch_size and params.batch_size > 0 and params.is_concurrently:
            # Fetch all pages concurrently
            single_result = await fetch_single(params)
            object_count = single_result.count
            log.info(f"Total count to fetch: {object_count}")
            total_count = 0
            page_number = 1
            page_size = params.batch_size
            pages = (object_count // page_size) + 1
            # Create tasks for all pages
            tasks: list[asyncio.Task[TListModel]] = []
            for page_number in range(1, pages + 1):
                paginated_params = params.model_copy()
                paginated_params.page_number = page_number
                paginated_params.page_size = page_size
                task: asyncio.Task[TListModel] = asyncio.create_task(
                    fetch_with_semaphore(paginated_params)
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
            return merged_models
        elif batch_size := params.batch_size:
            # Fetch all pages sequentially with batch size
            total_count = 0
            page_number = 1
            page_size = batch_size
            while True:
                paginated_params = params.model_copy()
                paginated_params.page_number = page_number
                paginated_params.page_size = page_size
                log.info(f"Fetching page {page_number} with size {page_size}...")
                result = await fetch_fn(paginated_params)
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

            return merged_models
        else:
            # Otherwise, fetch all items in a single request
            return await fetch_fn(params)
