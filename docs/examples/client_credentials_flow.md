# Client Credentials Flow Example

This example demonstrates how to use the Apaleo API Client with the OAuth2 Client Credentials flow. This flow is ideal for server-to-server communication where user interaction is not required.

```python {title="Minimal example using the Client Credentials flow"}
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
        service="Apaleo API Client - Client Credentials Flow",
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
