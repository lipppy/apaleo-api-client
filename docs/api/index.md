# API Reference Overview

This section provides comprehensive documentation for all Apaleo API endpoints supported by the SDK. The Apaleo API Client provides type-safe, async access to Apaleo's hospitality platform APIs through a unified Python interface.

## Documentation Structure

Each API documentation includes:

- **Swagger UI** link for interactive exploration of endpoints
- **Endpoint mapping** with HTTP method and URL path
- **SDK method signature** with typed parameters
- **Request parameters** with types, descriptions, and validation rules
- **Response schemas** with detailed data models
- **Usage examples** with practical code snippets
- **Error handling** information and possible exceptions

## Client Architecture

The SDK follows a hierarchical structure that mirrors Apaleo's API organization:

`<client>.<api_domain>.<version>.<resource>.<method>`

```python
# Main client entry point
client = ApaleoAPIClient(token_provider=token_provider)

# API domain access
client.core          # Core API (properties, inventory, rates)
client.identity      # Identity API (users, roles, invitations)
client.integration   # Integration API (external systems)
client.payment       # Payment API (transactions, methods)
client.webhook       # Webhook API (event subscriptions)
client.fiscalization # Fiscalization API (tax compliance)
client.profile       # Profile API (user profiles, preferences)
```

## Available APIs

### Core API

**Access:** `client.core.v1`

The Core API is the foundation of the Apaleo ecosystem, providing essential hospitality management functionality:

- **Property Management** - Create, configure, and manage hotel properties
- **Inventory Management** - Units (rooms, beds, parking), unit groups, and availability
- **Rate Plans** - Pricing strategies, rate restrictions, and dynamic pricing
- **Unit Attributes** - Amenities, features, and property characteristics
- **Unit Actions** - Operational commands for room management

**Documentation:** [Core API](core/inventory_v1.md)

### Identity API

**Access:** `client.identity.v1`

The Identity API manages authentication, authorization, and user administration within the Apaleo ecosystem:

- **User Management** - Account creation, profile updates, and user lifecycle
- **Role-Based Access Control** - Permission management and role assignments
- **Invitation System** - User onboarding and account provisioning
- **Authentication** - OAuth 2.0 flows and token management
- **Account Administration** - Multi-tenant account structure management

**Available Resources:**
- `client.identity.v1.identity` - Core identity management endpoints

**Documentation:** [Identity API](identity/identity_v1.md)

### Integration API

**Access:** `client.integration` *(Coming Soon)*

Provides connectivity and data exchange capabilities for third-party systems:

- **Channel Management** - OTA connections and distribution
- **PMS Integrations** - Property Management System connectivity
- **Revenue Management** - External revenue optimization tools
- **Reporting Integrations** - Business intelligence and analytics platforms

### Payment API

**Access:** `client.payment` *(Coming Soon)*

Handles financial transactions and payment processing:

- **Payment Methods** - Credit cards, digital wallets, bank transfers
- **Transaction Management** - Authorizations, captures, refunds, voids
- **Merchant Configuration** - Payment gateway setup and preferences
- **Compliance** - PCI DSS standards and regulatory requirements

### Webhook API

**Access:** `client.webhook` *(Coming Soon)*

Event-driven architecture for real-time integrations:

- **Event Subscriptions** - Configure webhook endpoints for specific events
- **Event Types** - Reservation changes, payment status, inventory updates
- **Delivery Management** - Retry logic, failure handling, and delivery confirmations
- **Security** - Signature verification and endpoint authentication

### Fiscalization API

**Access:** `client.fiscalization` *(Coming Soon)*

Tax compliance and fiscal reporting for various jurisdictions:

- **Tax Configuration** - Regional tax rules and calculation methods
- **Fiscal Receipts** - Government-compliant receipt generation
- **Reporting** - Tax authority submissions and compliance reports
- **Multi-jurisdiction** - Support for different national and local tax systems

### Profile API

**Access:** `client.profile` *(Coming Soon)*

User preference and profile management:

- **User Preferences** - Language, timezone, and notification settings
- **Profile Customization** - Dashboard layouts and feature preferences
- **Organizational Settings** - Company-wide defaults and policies
- **API Preferences** - Rate limiting, response formats, and integration settings

## Development Status

### Currently Available (v1)
- ✅ **Identity API** - Complete user and role management

### In Development
- 🚧 **Core API** - Additional v1 resources (rates, reservations, finance)
- 🚧 **Integration API** - Channel and PMS connectivity
- 🚧 **Payment API** - Transaction and payment method management

### Planned
- 📋 **Webhook API** - Event subscription and delivery
- 📋 **Fiscalization API** - Tax compliance and reporting
- 📋 **Profile API** - User and organizational preferences

## Common Patterns

### Async Operations

All SDK methods are async and should be awaited:

```python
# Fetch a property
property_data = await client.core.v1.inventory.get_property(property_id="BER")

# List entities with pagination
invitations = await client.identity.v1.identity.list_invitations(page_size=50)
```

### Uniform List Responses

All list endpoints' responses adjusted to a common structure with count metadata:


```python {title="Instead of..."}
# List of objects by object-specific key with count info
{
    "invitations": [...],
    "count": 100,
}

# or

# List of objects by object-specific key without count info
{
    "roles": [...],
}
```


```python {title="Now..."}
# List of objects by neutral key with count info
{
    "items": [Invitation],
    "count": 100,
}

# or

{
    "items": [Role],
    "count": 100,
}
```

### Concurrent Requests for List Endpoints

The SDK supports concurrent requests for improved performance when fetching paginated data:

```python
# Fetch multiple pages of invitations concurrently
params = InvitationListParams(batch_size=50, is_concurrently=True)
invitations = await client.identity.v1.identity.list_invitations(params)
```

### Error Handling
The SDK provides structured exceptions for different error scenarios:

```python
from apaleoapi.exceptions import ApaleoAPIError, AuthenticationError

try:
    property_data = await client.core.v1.inventory.get_property(property_id="INVALID")
except AuthenticationError:
    # Handle authentication failures
    pass
except ApaleoAPIError as e:
    # Handle general API errors
    print(f"API error: {e.status_code} - {e.detail}")
```

### Resource Cleanup
Always close the client when done to properly clean up resources:

```python
async with ApaleoAPIClient(token_provider=token_provider) as client:
    # Use client here
    property_data = await client.core.v1.inventory.get_property(property_id="BER")
# Client automatically closed

# Or manually
await client.aclose()
```
