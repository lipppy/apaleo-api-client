# Installation

Get started with Apaleo API Client quickly and easily. The library supports Python 3.10+ and can be installed using your preferred package manager.

## 📦 **Package Installation**

### **Using pip (recommended)**

```bash
pip install apaleo-api-client
```

### **Using Poetry**

```bash
poetry add apaleo-api-client
```

### **Using pipenv**

```bash
pipenv install apaleo-api-client
```

### **Using conda**

```bash
conda install -c conda-forge apaleo-api-client
```

## 🔧 **Development Installation**

For development or contributing to the project:

### **Clone the Repository**

```bash
git clone https://github.com/lipppy/apaleo-api-client.git
cd apaleo-api-client
```

### **Install with Poetry (Recommended)**

```bash
# Install with all development dependencies
poetry install --with dev,test,lint,docs

# Activate the virtual environment
poetry shell
```

### **Install with pip**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,test,lint,docs]"
```

## 🔍 **System Requirements**

### **Python Version**
- **Python 3.10** or higher
- **Python 3.13** is fully supported
- Tested on CPython (PyPy support coming soon)

### **Operating Systems**
- ✔️ Linux (Ubuntu, CentOS, Alpine)
- ✔️ macOS (Intel and Apple Silicon)
- ✔️ Windows (10, 11, Server)

### **Dependencies**

Core dependencies (automatically installed):

```
httpx>=0.28.1        # Async HTTP client
pydantic>=2.12.5     # Data validation and serialization
dacite>=1.9.2        # Dataclass conversion
httpx-retries>=0.4.6 # HTTP retry middleware
polyfactory>=3.3.0   # Testing factories
```

## 🗂️ **Verify Installation**

Test that the installation was successful:

```python
from apaleoapi import ApaleoAPIClient
from apaleoapi import __version__

print(f"Apaleo API Client version: {__version__}")

# Test client initialization (dry-run mode)
client = ApaleoAPIClient(
    client_id="test",
    client_secret="test",
    dry_run=True
)

print("Installation successful!")
```

## 🏡 **Getting API Credentials**

Before using the client, you'll need Apaleo API credentials:

### **1. Register with Apaleo**
1. Visit the [Apaleo Developer Portal](https://apaleo.dev)
2. Create a developer account or sign in
3. Navigate to "Applications" or "API Keys"

### **2. Create an Application**
1. Click "Create Application"
2. Enter your application details:
   - **Name**: Your application name
   - **Description**: Brief description of your integration
   - **Redirect URI**: For OAuth flows (if needed)

### **3. Get Your Credentials**
After creating the application, you'll receive:
- **Client ID**: Public identifier for your application
- **Client Secret**: Private secret (keep secure!)

### **4. Configure Scopes**
Select the appropriate API scopes for your use case:
- `core:read` - Read access to Core API
- `core:write` - Write access to Core API
- `identity:read` - Read access to Identity API
- Additional scopes as needed

## ⚙️ **Configuration**

### **Environment Variables**

Store your credentials securely using environment variables:

```bash
# .env file
APALEO_CLIENT_ID=your-client-id-here
APALEO_CLIENT_SECRET=your-client-secret-here
APALEO_TIMEOUT=30
APALEO_MAX_RETRIES=3
APALEO_MAX_CONCURRENT=5
```

Load them in your application:

```python
import os
from apaleoapi import ApaleoAPIClient

client = ApaleoAPIClient(
    client_id=os.getenv("APALEO_CLIENT_ID"),
    client_secret=os.getenv("APALEO_CLIENT_SECRET"),
    timeout=float(os.getenv("APALEO_TIMEOUT", 30)),
    retries=int(os.getenv("APALEO_MAX_RETRIES", 3)),
    max_concurrent=int(os.getenv("APALEO_MAX_CONCURRENT", 5))
)
```

### **Configuration File**

Alternatively, use a configuration file:

```yaml
# apaleo_config.yaml
apaleo:
  client_id: "your-client-id"
  client_secret: "your-client-secret"
  timeout: 30.0
  retries: 3
  max_concurrent: 5
  dry_run: false

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

```python
import yaml
from apaleoapi import ApaleoAPIClient

with open("apaleo_config.yaml") as f:
    config = yaml.safe_load(f)

client = ApaleoAPIClient(**config["apaleo"])
```

## 🛡️ **Security Best Practices**

### **Credential Management**
- ⚠️ **Never** commit credentials to version control
- Use environment variables or secure secret management
- Rotate credentials regularly
- Use different credentials for development/staging/production

### **Network Security**
- Always use HTTPS (enforced by default)
- Consider using a VPN for sensitive environments
- Monitor API access logs

### **Application Security**
- Validate all user inputs before API calls
- Implement proper error handling
- Log security events appropriately
- Follow the principle of least privilege for API scopes

## 🔥 **Quick Start Example**

Put it all together with a complete example:

```python
import asyncio
import os
from apaleoapi import ApaleoAPIClient
from apaleoapi.apaleo.core.v1.dataclasses.inventory import PropertyListParams

async def main():
    # Initialize client with environment variables
    client = ApaleoAPIClient(
        client_id=os.getenv("APALEO_CLIENT_ID"),
        client_secret=os.getenv("APALEO_CLIENT_SECRET")
    )

    try:
        # Fetch first 10 properties
        params = PropertyListParams(page_size=10)
        properties = await client.core.v1.inventory.list_properties(params)

        print(f"Found {properties.count} total properties")
        for prop in properties.items:
            print(f"- {prop.name} ({prop.code})")

    finally:
        # Always clean up
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔄 **Upgrading**

### **Check Current Version**

```python
from apaleoapi import __version__
print(__version__)
```

### **Upgrade to Latest**

```bash
pip install --upgrade apaleo-api-client
```

### **Upgrade with Poetry**

```bash
poetry update apaleo-api-client
```

## 🎆 **Next Steps**

Now that you have the library installed:

1. **[Learn the basics](why.md)** - Understand key concepts
2. **[Explore examples](../examples/client.md)** - See practical usage patterns
3. **[Read the API docs](../api/core.md)** - Dive into the full API reference
4. **[Join the community](contributing.md)** - Get help and contribute

---

**Having issues with installation?** Check our [troubleshooting guide]( troubleshooting.md) or [open an issue](https://github.com/lipppy/apaleo-api-client/issues).
