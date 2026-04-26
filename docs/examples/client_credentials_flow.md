# Client Credentials Flow Example

This example demonstrates how to use the Apaleo API Client with the OAuth2 Client Credentials flow. This flow is ideal for server-to-server communication where user interaction is not required.

```python {title="Minimal example using the Client Credentials flow"}
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
