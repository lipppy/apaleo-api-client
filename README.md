# Apaleo API Client - Python SDK

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
- **Flexible request inputs** - Pass params and payloads as typed dataclasses or plain dictionaries
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

### Basic Example Client Credentials

```python
import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Basic Example Client Credentials - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider)

    # Fetch a property by its ID
    property_berlin = await client.core.v1.inventory.get_property(
        property_id="BER"
    )
    print(property_berlin)
    # > Property(id='BER', code='BER', name={'en': 'Hotel Berlin'}, ...)

    print(type(property_berlin))
    # > <class 'apaleoapi.apaleo.core.v1.contracts.inventory.response.Property'>

    print(property_berlin.id)
    # > BER

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```

### Flexible Request Inputs

Request params and payloads can be passed either as the SDK's typed dataclasses or as plain dictionaries. JSON Patch operations also accept `list[dict[str, Any]]` for convenience, while still going through the same validation layer.

```python
import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.core.v1.inventory import PropertyListParams

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Flexible Request Inputs Example - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider)

    # Typed params
    params_typed = PropertyListParams(
        country_code=["DE", "AT"], include_archived=False
    )
    properties_1 = await client.core.v1.inventory.list_properties(
        params=params_typed
    )
    print("Found properties (typed params):", len(properties_1.items))
    # > Found properties (typed params): N>

    # Equivalent dict params with snake_case keys
    params_dict = {"country_code": ["DE", "AT"], "include_archived": False}
    properties_2 = await client.core.v1.inventory.list_properties(
        params=params_dict
    )
    print("Found properties (dict params):", len(properties_2.items))
    # > Found properties (dict params): N>

    # Equivalent dict params with alias keys (Apaleo API uses camelCase)
    params_alias = {"countryCode": ["DE", "AT"], "includeArchived": False}
    properties_3 = await client.core.v1.inventory.list_properties(
        params=params_alias
    )
    print("Found properties (alias params):", len(properties_3.items))
    # > Found properties (alias params): N>

    # You can also mix snake_case and camelCase keys if you like,
    # the client will handle the conversion
    params_mixed = {"country_code": ["DE", "AT"], "includeArchived": False}
    properties_4 = await client.core.v1.inventory.list_properties(
        params=params_mixed
    )
    print("Found properties (mixed params):", len(properties_4.items))
    # > Found properties (mixed params): N>

    # All four calls should yield the same result
    assert properties_1 == properties_2 == properties_3 == properties_4

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```

**Note: The above examples assume you have the appropriate API credentials and access to the Apaleo API. Replace the parameters and payloads with valid values according to your account and API permissions.*

#### Patch Payloads with Flexible Input

```python
import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.common import Operation, OperationOp

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Flexible Request Inputs Example - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider)

    # Typed params
    property_id = "BER"
    property_berlin_before = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_before = (
        property_berlin_before.description.get("en", "")
        if property_berlin_before.description
        else ""
    )
    print(
        "Property description (before update):",
        property_description_before or "<no description>",
    )
    # > Property description (before update): <no description>

    property_description_after = "Added description for Berlin property"
    # Using JSON Patch operations for the update,
    # which allows for flexible request inputs
    # Do not forget to use list of operations as payload for the update method,
    # even if you have just one operation to perform
    operations_params = [
        Operation(
            op=OperationOp.ADD,
            path="/description/en",
            value=property_description_after,
        )
    ]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=operations_params
    )
    property_berlin_after = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after = (
        property_berlin_after.description.get("en", "")
        if property_berlin_after.description
        else ""
    )
    print(
        "Property description (after update):",
        property_description_after or "<no description>",
    )
    # > Property description (after update): Added description for Berlin property>

    # Revert the change to keep the test idempotent, use dict payload for that
    revert_operations_params = [{"op": "remove", "path": "/description/en"}]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=revert_operations_params
    )
    property_berlin_after_revert = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after_revert = (
        property_berlin_after_revert.description.get("en", "")
        if property_berlin_after_revert.description
        else ""
    )
    print(
        "Property description (after revert):",
        property_description_after_revert or "<no description>",
    )
    # > Property description (after revert): <no description>

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```

## Concurrent Fetching & Resilience

The client supports concurrent fetching of resources to improve performance when dealing with large datasets. It also includes basic retry and token refresh handling for short-lived failures, improving robustness in your applications.

All list type endpoints which support concurrent fetching you can enable by passing `is_concurrently=True` and `batch_size` in the parameters. The client will automatically handle pagination and fetch multiple pages concurrently up to the configured `max_concurrent` limit.

The example below demonstrates concurrent fetching of properties with flexible request parameters:
- client is configured with `max_concurrent=3` to limit concurrency to 3 simultaneous requests
- `list_properties` is called with `is_concurrently=True` and `batch_size=1` to fetch one property per page and enable concurrent fetching of pages
- The client will log the acquisition and release of semaphores for each page, showing how it manages concurrency while fetching the paginated results.
- The final output will show the total number of properties found across all pages.
- The order of items in the final result may not match the order of pages fetched concurrently. If you need results in a specific order, consider fetching pages sequentially or implementing additional sorting logic after fetching.

**Note: Concurrent fetching can lead to faster data retrieval but may also increase the risk of hitting API rate limits. Use with caution and consider implementing retry logic to handle potential rate limit responses.**

```python
import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.common import Operation, OperationOp

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Flexible Request Inputs Example - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider)

    # Typed params
    property_id = "BER"
    property_berlin_before = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_before = (
        property_berlin_before.description.get("en", "")
        if property_berlin_before.description
        else ""
    )
    print(
        "Property description (before update):",
        property_description_before or "<no description>",
    )
    # > Property description (before update): <no description>

    property_description_after = "Added description for Berlin property"
    # Using JSON Patch operations for the update,
    # which allows for flexible request inputs
    # Do not forget to use list of operations as payload for the update method,
    # even if you have just one operation to perform
    operations_params = [
        Operation(
            op=OperationOp.ADD,
            path="/description/en",
            value=property_description_after,
        )
    ]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=operations_params
    )
    property_berlin_after = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after = (
        property_berlin_after.description.get("en", "")
        if property_berlin_after.description
        else ""
    )
    print(
        "Property description (after update):",
        property_description_after or "<no description>",
    )
    # > Property description (after update): Added description for Berlin property>

    # Revert the change to keep the test idempotent, use dict payload for that
    revert_operations_params = [{"op": "remove", "path": "/description/en"}]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=revert_operations_params
    )
    property_berlin_after_revert = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after_revert = (
        property_berlin_after_revert.description.get("en", "")
        if property_berlin_after_revert.description
        else ""
    )
    print(
        "Property description (after revert):",
        property_description_after_revert or "<no description>",
    )
    # > Property description (after revert): <no description>

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing

For guidance on setting up a development environment and how to make a
[Contributing to Apaleo API Client](https://lipppy.github.io/apaleo-api-client/main/contributing/).

## Reporting a Security Vulnerability

See our [security policy](https://github.com/lipppy/apaleo-api-client/security/policy).

## About the Author

The author has a background in meteorology and hydrology with 10+ years of full-stack web development and 5+ years specializing in Python. Currently working in the hospitality domain and actively integrating with Apaleo APIs, this project began as a way to eliminate repetitive API implementation work and provide Python developers with modern, type-safe Python bindings for the Apaleo API.

This is the author's first library published on PyPI. As a hobby project, support and development pace depend on availability beyond work commitments.
