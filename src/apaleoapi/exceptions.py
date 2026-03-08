from typing import List, Optional

import httpx


class APIError(Exception):
    """Base API exception."""

    def __init__(self, message: str, response: httpx.Response):
        self.response = response
        self.status_code = response.status_code
        super().__init__(message)


class BadRequestError(APIError):
    pass


class UnauthorizedError(APIError):
    pass


class ForbiddenError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ValidationError(APIError):
    def __init__(self, message: str, response: httpx.Response, errors: Optional[List[str]] = None):
        self.errors = errors or []
        super().__init__(message, response)


class ClientClosedRequestError(APIError):
    pass


class InternalServerError(APIError):
    pass


class ServiceUnavailableError(APIError):
    pass


class DeleteResourceError(APIError):
    pass
