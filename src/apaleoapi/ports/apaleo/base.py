from apaleoapi.logging import get_logger
from apaleoapi.ports.http.response_handler import ResponseHandlerPort
from apaleoapi.ports.http.response_validator import ResponseValidatorPort
from apaleoapi.ports.http.transport import AsyncTransportPort
from apaleoapi.ports.validation.url_path_validator import URLPathValidatorPort

log = get_logger(__name__)


class BasePort:
    def __init__(
        self,
        transport: AsyncTransportPort,
        response_handler: ResponseHandlerPort,
        response_validator: ResponseValidatorPort,
        url_path_validator: URLPathValidatorPort,
        max_concurrent: int,
        dry_run: bool = False,
    ) -> None:
        self._t = transport
        self._response_handler = response_handler
        self._response_validator = response_validator
        self._url_path_validator = url_path_validator
        self._max_concurrent = max_concurrent
        self._dry_run = dry_run
