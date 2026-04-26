import os

import pytest

from apaleoapi.client import ApaleoAPIClient
from apaleoapi.http.auth import OAuth2ClientCredentialsProvider


@pytest.fixture
def client_valid() -> ApaleoAPIClient:
    """Fixture for providing a valid ApaleoAPIClient instance for tests."""
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.environ["APALEO_CLIENT_ID_CLIENT_CREDENTIALS"],
        client_secret=os.environ["APALEO_CLIENT_SECRET_CLIENT_CREDENTIALS"],
        service="Apaleo API Client - Integration Tests - Valid Client",
    )
    return ApaleoAPIClient(token_provider=token_provider)


@pytest.fixture
def client_invalid() -> ApaleoAPIClient:
    """Fixture for providing an invalid ApaleoAPIClient instance for tests."""
    token_provider = OAuth2ClientCredentialsProvider(
        client_id="invalid-client-id-client-credentials",
        client_secret="invalid-client-secret-client-credentials",
        service="Apaleo API Client - Integration Tests - Invalid Client",
    )
    return ApaleoAPIClient(token_provider=token_provider)
