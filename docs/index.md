# Welcome to Apaleo API Client

A **type-safe, async Python SDK** for the Apaleo API built on **Pydantic v2** and **httpx**. Provides seamless integration with Apaleo's hospitality platform. Fast, easy to use, and fully documented.

## What is Apaleo API Client?

The Apaleo API Client is a production-ready Python library that wraps the Apaleo Swagger API with a modern, developer-friendly interface. Built for high-performance async operations, it provides:

- **🔐 OAuth2 Authentication** - Automatic token management with refresh capabilities, both client credentials and authorization code flow are supported
- **⚡ Async/Await Support** - Built for high-performance concurrent operations
- **📝 Type Safety** - Comprehensive Pydantic models for all requests and responses
- **🛡️ Error Handling** - Domain-specific exceptions with detailed error information
- **📄 Pagination** - Smart concurrent batch fetching for large datasets
- **🔧 Extensible** - Modular adapter pattern supporting all Apaleo API domains

## Quick Start

Get started with Apaleo API Client in just a few lines:

```python
from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider


# Create a token provider with your API credentials
token_provider = OAuth2ClientCredentialsProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    service="My Application"
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

# Clean up
await client.aclose()
```

For more examples and detailed documentation, see the [API Reference](api/index.md) section.

## Key Features

### **Comprehensive API Coverage**
Supports all major Apaleo API domains:

- **Core API**: Properties, inventory, rates, and units management
- **Identity API**: User management, invitations, roles
- **Payment API**: Payment processing and transaction handling
- **Webhook API**: Event-driven integrations
- **Integration API**: Third-party system connections
- **Fiscalization API**: Tax and compliance management
- **Profile API**: User profile and preference management

### **Developer Experience**
- **Type Complete**: Full type hints and IDE autocompletion
- **Async Native**: Built on `httpx` for optimal performance
- **Testing Ready**: Comprehensive test coverage and dry-run mode
- **Well Documented**: Detailed API reference and examples

### **Production Ready**
- **Robust Error Handling**: Typed exceptions for all HTTP status codes
- **Automatic Retries**: Configurable retry logic for transient failures
- **Rate Limiting**: Built-in concurrent request management
- **Logging Integration**: Comprehensive logging for debugging and monitoring

## Supported APIs

The client provides access to these Apaleo API endpoints:

| API Domain | Base URL | Version | Status | Coverage |
|------------|----------|---------|--------|----------|
| Core | `https://api.apaleo.com/` | V1 | 🔧 In Progress | <span style="color: cyan;">1%</span> |
| Identity | `https://identity.apaleo.com/` | V1 | ✅ Implemented | <span style="color: lime;">100%</span> |
| Payment | `https://payment.apaleo.com/` | V1 | 🔧 Planned | <span style="color: tomato;">0%</span> |
| Webhook | `https://webhook.apaleo.com/` | V1 | 🔧 Planned | <span style="color: tomato;">0%</span> |
| Integration | `https://integration.apaleo.com/` | V1 | 📋 Planned | <span style="color: tomato;">0%</span> |
| Fiscalization | `https://fiscalization.apaleo.com/` | V1 | 📋 Planned | <span style="color: tomato;">0%</span> |
| Profile | `https://profile.apaleo.com/` | V1 | 📋 Planned | <span style="color: tomato;">0%</span> |

## Next Steps

- **[Why Apaleo API Client?](main/why.md)** - Learn about the benefits and use cases
- **[Installation](main/install.md)** - Install and set up the library
- **[API Reference](api/index.md)** - Explore detailed documentation for all endpoints
- **[Contributing](main/contributing.md)** - Help improve the library

## Community & Support

- **GitHub**: [lipppy/apaleo-api-client](https://github.com/lipppy/apaleo-api-client)
- **Issues**: Report bugs and request features on [GitHub](https://github.com/lipppy/apaleo-api-client/issues)
- **Discussions**: Join the community discussions on [GitHub](https://github.com/lipppy/apaleo-api-client/discussions)

---

Ready to experience the benefits? **[Why Apaleo API Client? →](main/why.md)**
