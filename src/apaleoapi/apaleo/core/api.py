# Core API


from apaleoapi.apaleo.core.v1.apis.inventory import CoreV1InventoryResource
from apaleoapi.http.transport import AuthenticatedTransport
from apaleoapi.ports.apaleo.base import BasePort
from apaleoapi.ports.http.response_handler import ResponseHandlerPort
from apaleoapi.ports.http.response_validator import ResponseValidatorPort
from apaleoapi.ports.validation.url_path_validator import URLPathValidatorPort


class CoreAPI(BasePort):
    """Top-level entry point for the entire Core API domain"""

    def __init__(
        self,
        transport: AuthenticatedTransport,
        response_handler: ResponseHandlerPort,
        response_validator: ResponseValidatorPort,
        url_path_validator: URLPathValidatorPort,
        max_concurrent: int,
        dry_run: bool,
    ) -> None:
        super().__init__(
            transport=transport,
            response_handler=response_handler,
            response_validator=response_validator,
            url_path_validator=url_path_validator,
            max_concurrent=max_concurrent,
            dry_run=dry_run,
        )
        self.v1 = CoreV1Version(
            transport=transport,
            response_handler=response_handler,
            response_validator=response_validator,
            url_path_validator=url_path_validator,
            max_concurrent=max_concurrent,
            dry_run=dry_run,
        )
        self.nsfw = CoreNSFWVersion(
            transport=transport,
            response_handler=response_handler,
            response_validator=response_validator,
            url_path_validator=url_path_validator,
            max_concurrent=max_concurrent,
            dry_run=dry_run,
        )


class CoreV1Version(BasePort):
    """Version-specific coordinator for v1 endpoints"""

    def __init__(
        self,
        transport: AuthenticatedTransport,
        response_handler: ResponseHandlerPort,
        response_validator: ResponseValidatorPort,
        url_path_validator: URLPathValidatorPort,
        max_concurrent: int,
        dry_run: bool,
    ) -> None:
        self.inventory = CoreV1InventoryResource(
            transport=transport,
            response_handler=response_handler,
            response_validator=response_validator,
            url_path_validator=url_path_validator,
            max_concurrent=max_concurrent,
            dry_run=dry_run,
        )


class CoreNSFWVersion(BasePort):
    """Version-specific coordinator for nsfw endpoints."""

    def __init__(
        self,
        transport: AuthenticatedTransport,
        response_handler: ResponseHandlerPort,
        response_validator: ResponseValidatorPort,
        url_path_validator: URLPathValidatorPort,
        max_concurrent: int,
        dry_run: bool,
    ) -> None:
        pass
