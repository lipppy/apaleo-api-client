# Apaleo API Client

[![CI](https://img.shields.io/github/actions/workflow/status/lipppy/apaleo-api-client/tests.yml?branch=main&logo=github&label=CI)](https://github.com/lipppy/apaleo-api-client/actions?query=event%3Apush+branch%3Amain+workflow%3ATests)
[![Coverage](https://codecov.io/github/lipppy/apaleo-api-client/coverage.svg)](https://codecov.io/github/lipppy/apaleo-api-client)
[![pypi](https://img.shields.io/pypi/v/apaleo-api-client.svg)](https://pypi.python.org/pypi/apaleo-api-client)
[![downloads](https://static.pepy.tech/badge/apaleo-api-client/month)](https://pepy.tech/project/apaleo-api-client)
[![versions](https://img.shields.io/pypi/pyversions/apaleo-api-client.svg)](https://github.com/lipppy/apaleo-api-client/blob/main/pyproject.toml#L15)
[![license](https://img.shields.io/github/license/lipppy/apaleo-api-client.svg)](https://github.com/lipppy/apaleo-api-client/blob/main/LICENSE)

Python SDK for the Apaleo API. Provides a type-safe, async client for seamless integration with Apaleo's hospitality platform. Built on Pydantic v2 and httpx. Fast, easy to use, and fully documented.

## Help

See [documentation](https://lipppy.github.io/apaleo-api-client/) for more details.

## Features

This SDK is actively under development with the goal of providing full coverage of the Apaleo API Swagger specifications focusing on `v1` but with the capability and intention to expand to other versions in the future.

Current status:

- **Type-safe abstractions** - Full type hints and Pydantic models for implemented resources
- **Async/await support** - Non-blocking I/O for high-performance applications
- **Authentication handling** - Built-in support for OAuth 2.0 flows (Client Credentials, Authorization Code)
- **Pagination** - Smart concurrent batch fetching for large datasets
- **Integration-tested** - Implemented endpoints validated against a DEV instance
- **Documentation-first** - Usage examples and docs evolving alongside feature coverage

## Installation

Install using `pip install -U apaleo-api-client` or `poetry add apaleo-api-client`.
For more installation options to make Apaleo API Client even faster,
see the [Installation](https://lipppy.github.io/apaleo-api-client/main/install/) section in the documentation.

## Code Examples

- [OAuth 2.0 - Client credentials grant flow](https://apaleo.dev/guides/oauth-connection/simple-client.html)
- [OAuth 2.0 - Authorization code grant flow](https://apaleo.dev/guides/oauth-connection/auth-code-grant.html)

### Client Credentials

```python
from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider


# Create a token provider with your API credentials
token_provider = OAuth2ClientCredentialsProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    service="Apaleo API Client - Client Credentials Flow"
)

# Create an instance of the client
client = ApaleoAPIClient(token_provider=token_provider)

# Fetch a property by its ID
property_berlin = await client.core.v1.inventory.get_property(property_id="BER")
print(property_berlin)
#> Property id=BER name='Berlin Hotel' address='123 Berlin St.'
print(type(property_berlin))
#> <class 'apaleo_api_client.core.v1.inventory.Property'>

print(property_berlin.id)
#> BER
```

## Contributing

For guidance on setting up a development environment and how to make a
[Contributing to Apaleo API Client](https://lipppy.github.io/apaleo-api-client/main/contributing/).

## Reporting a Security Vulnerability

See our [security policy](https://github.com/lipppy/apaleo-api-client/security/policy).

## About the Author

The author has a background in meteorology and hydrology with 10+ years of full-stack web development and 5+ years specializing in Python. Currently working in the hospitality domain and actively integrating with Apaleo APIs, this project began as a way to eliminate repetitive API implementation work and provide Python developers with modern, type-safe Python bindings for the Apaleo API.

This is the author's first library published on PyPI. As a hobby project, support and development pace depend on availability beyond work commitments.
