# Why use Apaleo API Client?

The Apaleo API Client provides a modern, developer-friendly way to integrate with Apaleo's hospitality platform. Here's why you should choose it over direct API calls or other integration methods.

## 🚀 **Performance & Efficiency**

### **Async-First Architecture**
- Built on `httpx` for high-performance concurrent operations
- Native `async/await` support for non-blocking I/O
- Concurrent request batching for pagination

```python
# Fetch multiple pages concurrently
properties = await client.core.v1.inventory.list_properties(
    PropertyListParams(is_concurrently=True, batch_size=100)
)
```

### **Smart Pagination**
- Automatic pagination handling with concurrent fetching
- Configurable batch sizes for optimal performance
- Built-in memory management for large datasets

## 🛡️ **Reliability & Robustness**

### **Comprehensive Error Handling**
- Typed exceptions for all HTTP status codes
- Detailed error messages with context
- Graceful handling of API rate limits and transient failures

```python
from apaleoapi.exceptions import ValidationError, NotFoundError

try:
    property = await client.core.v1.inventory.get_property("invalid-id")
except NotFoundError:
    print("Property not found")
except ValidationError as e:
    print(f"Invalid request: {e.message}")
```

### **Automatic Token Management**
- OAuth2 Client Credentials flow with automatic refresh
- Token caching and expiry tracking
- Seamless handling of 401 responses

### **Built-in Retries**
- Configurable retry logic for transient failures
- Exponential backoff with jitter
- Respect for Retry-After headers

## 📝 **Type Safety & Developer Experience**

### **Complete Type Coverage**
- Full type hints for all methods and responses
- Pydantic models for request/response validation
- IDE autocompletion and error detection

```python
# Type-safe parameter construction
params = PropertyListParams(
    page_number=1,          # int
    page_size=50,           # int
    include_archived=True,  # Optional[bool]
)

# Typed response handling
properties: PropertyList = await client.core.v1.inventory.list_properties(params)
for property: PropertyItem in properties.items:
    print(property.name)  # IDE knows this is a str
```

!!! note
    Apaleo's models may have field names that conflict with Python built-in function names, variable names, or keywords. Use caution when naming your variables or consider using aliases to avoid conflicts. For example, if a model has a field named `property`, you can use an alias like `from builtins import property as property_alias` in your code to prevent shadowing the built-in `@property` decorator.



### **Rich Data Models**
- Structured dataclasses for all domain objects
- Automatic serialization/deserialization
- Validation with detailed error messages

## 🛠️ **Development & Testing**

### **Dry-Run Mode**
Perfect for development and testing:

```python
# No actual API calls made
client = ApaleoAPIClient(..., dry_run=True)
properties = await client.core.v1.inventory.list_properties()
# Returns empty PropertyList for testing
```

### **Comprehensive Logging**
- Detailed request/response logging
- Configurable log levels
- Integration with Python's standard logging module

```python
from apaleoapi.logging import setup_logging

logger = setup_logging(level="DEBUG")
# See all HTTP requests, responses, and timing information
```

### **Testing Support**
- Mock-friendly design with dependency injection
- Async test patterns with pytest-asyncio
- Factory classes for test data generation

## 🏢 **Enterprise Ready**

### **Production Deployment**
- Configurable timeouts and connection limits
- Memory-efficient streaming for large responses
- Monitoring and observability hooks

### **Security**
- Secure credential handling
- TLS/SSL verification by default
- No credential logging in production mode

### **Scalability**
- Concurrent request limiting to respect API quotas
- Efficient connection pooling
- Horizontal scaling support

## 🎓 **Compared to Alternatives**

### **vs. Direct HTTP Calls**
✔️ No manual token management
✔️ Built-in error handling and retries
✔️ Type safety and validation
✔️ Pagination automation
✔️ Consistent API interface

### **vs. Generic API Clients**
✔️ Domain-specific error types
✔️ Apaleo-optimized request patterns
✔️ Built-in knowledge of API quirks
✔️ Specialized data models
✔️ Hotel industry domain knowledge

### **vs. Custom Wrappers**
✔️ Production-tested reliability
✔️ Comprehensive test coverage
✔️ Active maintenance and updates
✔️ Community support and documentation
✔️ Performance optimizations

## 📊 **Use Cases**

### **Property Management Systems (PMS)**
- Sync property data and availability
- Manage rates and inventory
- Handle reservations and guest information

### **Channel Managers**
- Distribute inventory across multiple channels
- Real-time rate and availability updates
- Central reservation management

### **Revenue Management**
- Analyze booking patterns and performance
- Dynamic pricing optimization
- Competitive market analysis

### **Business Intelligence**
- Extract data for reporting and analytics
- Monitor KPIs and performance metrics
- Historical trend analysis

### **Integration Platforms**
- Connect Apaleo with other hospitality systems
- Data synchronization between platforms
- Workflow automation

---

Ready to experience the benefits? **[Install Apaleo API Client →](install.md)**
