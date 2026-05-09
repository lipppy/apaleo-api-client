import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest
import respx

from apaleoapi.http.transport import AuthenticatedTransport

pytestmark = [pytest.mark.unit, pytest.mark.asyncio, pytest.mark.slow]

FAKE_HOST = "https://fake-host"

ALLOWED_STATUS_CODES = {
    429,
    502,
    503,
    504,
}
ALLOWED_METHODS = {
    "HEAD",
    "GET",
    "PUT",
    "DELETE",
    "OPTIONS",
    # "TRACE" is not supported by httpx_mock, so we will test it separately
}
NOT_ALLOWED_METHODS = {
    "POST",
    "PATCH",
}
METHODS = ALLOWED_METHODS | NOT_ALLOWED_METHODS
ALLOWED_EXCEPTIONS = {httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError}


class TestAuthenticatedTransportRetries:
    """
    Test cases for retry logic in AuthenticatedTransport.

    These tests verify that the transport correctly retries requests based on
    the configured retryable status codes.

    Retryable status codes are hardcoded by the httpx_retries library per default but customizable.
    The default retryable status codes include:
        - 429 Too Many Requests
        - 502 Bad Gateway
        - 503 Service Unavailable
        - 504 Gateway Timeout
    Retryable methods are hardcoded by the httpx_retries library per default but customizable.
    The default retryable methods include:
        - HEAD
        - GET
        - PUT
        - DELETE
        - OPTIONS
        - TRACE
    """

    def setup_method(self) -> None:
        token_provider = AsyncMock()
        token_provider.auth_header.return_value = {"Authorization": "Bearer test-token"}

        self.transport = AuthenticatedTransport(
            base_url=FAKE_HOST,
            token_provider=token_provider,
            retries=3,
        )

    def teardown_method(self) -> None:
        asyncio.run(self.transport.aclose())

    @pytest.mark.parametrize(
        "side_effects,last_status_code,expected_calls",
        [
            # 2 retryable failures followed by a success
            (
                [
                    httpx.Response(429),
                    httpx.Response(502),
                    httpx.Response(200),
                ],
                200,
                3,
            ),
            # 1 retryable failure followed by a success
            (
                [
                    httpx.Response(502),
                    httpx.Response(201),
                ],
                201,
                2,
            ),
            # 1 retryable failure followed by a success, third response never reached due to success
            (
                [
                    httpx.Response(502),
                    httpx.Response(204),
                    httpx.Response(404),
                ],
                204,
                2,
            ),
            # All non-retryable failures, should not retry and return the first response
            (
                [
                    httpx.Response(400),
                    httpx.Response(422),
                    httpx.Response(404),
                ],
                400,
                1,
            ),
            # All retryable failures, should retry the max number of times and return the last
            (
                [
                    httpx.Response(502),
                    httpx.Response(503),
                    httpx.Response(504),
                    httpx.Response(500),
                    httpx.Response(502),  # Not reached due to max retries
                ],
                500,
                4,
            ),
            # Retryable failures, status codes and exceptions mixed, should retry on both
            (
                [
                    httpx.Response(502),
                    httpx.TimeoutException("Request timed out"),
                    httpx.RemoteProtocolError("Remote protocol error"),
                    httpx.Response(200),
                ],
                200,
                4,
            ),
        ],
    )
    async def test_authenticated_transport_with_retry_scenario(
        self,
        side_effects: list[httpx.Response | Exception],
        last_status_code: int,
        expected_calls: int,
    ) -> None:
        """
        Test that the transport retries on retryable status codes and eventually
        returns the successful response.
        """
        for method in METHODS:
            with respx.mock(base_url=FAKE_HOST) as mock:
                route = getattr(mock, method.lower())("/health").mock(
                    side_effect=list(side_effects)
                )

                response = await self.transport.request(method, "/health")

                if method in ALLOWED_METHODS:
                    assert response.status_code == last_status_code
                    assert route.calls.call_count == expected_calls
                else:
                    # For unsupported methods, it should not retry and return the first response
                    assert isinstance(side_effects[0], httpx.Response)
                    assert response.status_code == side_effects[0].status_code
                    assert route.calls.call_count == 1

    @pytest.mark.parametrize("method", METHODS)  # Test all methods with retryable exceptions
    async def test_authenticated_transport_with_retries_for_exceptions(self, method: str) -> None:
        """
        Test that the transport retries on retryable exceptions and eventually
        raises the exception after max retries.
        """
        with respx.mock(base_url=FAKE_HOST) as mock:
            route = getattr(mock, method.lower())("/health").mock(
                side_effect=httpx.TimeoutException("Request timed out")
            )

            with pytest.raises(httpx.TimeoutException):
                await self.transport.request(method, "/health")

            if method in ALLOWED_METHODS:
                assert route.calls.call_count == 4  # Initial call + 3 retries
            else:
                assert route.calls.call_count == 1  # No retries for unsupported methods

    @pytest.mark.parametrize("method", METHODS)  # Test all methods with non-retryable exceptions
    async def test_authenticated_transport_with_non_retryable_exceptions(self, method: str) -> None:
        """
        Test that the transport does not retry on non-retryable exceptions and
        raises the exception immediately.
        """

        with respx.mock(base_url=FAKE_HOST) as mock:
            route = getattr(mock, method.lower())("/health").mock(
                side_effect=httpx.ProxyError("Proxy error")
            )

            with pytest.raises(httpx.ProxyError):
                await self.transport.request(method, "/health")

            if method in ALLOWED_METHODS:
                assert route.calls.call_count == 1  # No retries for non-retryable exceptions
            else:
                assert route.calls.call_count == 1  # No retries for unsupported methods
