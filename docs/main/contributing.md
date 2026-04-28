# Contributing to Apaleo API Client

We welcome contributions to the Apaleo API Client! Whether you're fixing bugs, adding features, improving documentation, or helping with testing, your contributions are valued.

## Issues

Questions, feature requests, and bug reports are welcome through [GitHub Discussions or Issues](https://github.com/lipppy/apaleo-api-client/discussions).

If you need to report a security vulnerability, please use the process described in our [Security Policy](https://github.com/lipppy/apaleo-api-client/SECURITY.md).

To help us investigate issues efficiently, please include the output of the following command whenever relevant:

```bash
poetry run python -c \
    "import src.apaleoapi.utils; print(src.apaleoapi.utils.version_info())"
```

Please include this information whenever possible, unless the package cannot be installed or the details are clearly unrelated to your request.

## Quick Start for Contributors

### Prerequisites
- Python 3.10 or higher
    - Recommended: Python 3.12 for development
    - Supported: Python 3.10, 3.11, 3.12, 3.13
    - For `nox` testing: Python 3.10-3.13
- Git
- Poetry (for development)
- Python `invoke` (for running tasks)

### Development Environment

```bash
# Fork the repository on GitHub first, then clone
git clone https://github.com/<your-username>/apaleo-api-client.git
cd apaleo-api-client

# Lock dependencies and create virtual environment
poetry lock

# Install with all development dependencies
poetry install --with dev,test,lint,docs

# Activate the virtual environment
poetry shell

# Verify installation
inv help
```

### Check Everything Works

```bash
# Run tests
inv test

# Run linting
inv lint

# Format code
inv format

# Build and serve documentation
inv serve-docs
```

### Make Your Changes

```bash
# Create a feature branch
git checkout -b feature/AAC-<issue-number>-your-feature-name

# Make your changes
# ...

# Run tests and linting
inv test
inv lint

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/AAC-<issue-number>-your-feature-name
```

### Submit a Pull Request

1. Go to the GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Wait for review feedback

## Project Structure

 Understanding the codebase structure:

```
src/apaleoapi/
├── client.py                  # Main ApaleoAPIClient
├── constants.py               # API endpoints and constants
├── exceptions.py              # Custom exception classes
├── logging.py                 # Logging configuration
├── typing.py                  # Type definitions
│
├── apaleo/                    # API domain modules
│   ├── common/                # Common models and utilities
│   ├── core/                  # Core API (properties, inventory)
│   ├── identity/              # Identity & authentication
│   ├── payment/               # Payment processing
│   ├── webhook/               # Webhook management
│   ├── integration/           # Third-party integrations
│   ├── fiscalization/         # Tax and compliance
│   └── profile/               # User profiles
│
├── http/                      # HTTP layer
│   ├── auth.py                # OAuth2 authentication
│   └── transport.py           # HTTP transport layer
│
├── ports/                     # Abstraction layer
│   ├── apaleo/                # Apaleo API ports
│   ├── http/                  # HTTP ports
│   └── client.py              # Client ports
│
└── services/                  # Support services
    ├── list_fetcher.py        # Pagination handling
    ├── response_handler.py    # Response processing
    ├── response_validator.py  # Response validation
    └── url_path_validator.py  # URL path validation
```

## Development Workflow

### Available Tasks (via `invoke`)

| Task Name | Description |
|-----------|-------------|
| `inv help` | Show all available tasks |
| `inv test` | Run tests with pytest |
| `inv test-nox` | Test across Python 3.10-3.13 |
| `inv test-integration` | Run integration tests against DEV instance |
| `inv lint` | Run all linters (ruff, mypy, etc.) |
| `inv format` | Format code (ruff format, isort) |
| `inv check` | Check code quality without fixing |
| `inv serve-docs` | Build and serve documentation |
| `inv publish-docs` | Build and publish documentation to GitHub Pages |
| `inv build-checked` | Build package with checks (type checking, linting) |
| `inv increase-version` | Bump version (major, minor, patch) |
| `inv clean` | Clean cache and temporary files |
| `inv clean-docs` | Clean documentation build artifacts |
| `inv clean-build` | Clean all build artifacts |

!!! note
    The **integration test** `inv test-integration` require valid Apaleo API credentials (only client credentials) and will make real API calls to the instance your credentials are associated with. Use with caution and never run integration tests against production credentials.

### Code Style

We use these tools for code quality:

- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **isort**: Import sorting
- **pytest**: Testing framework

#### Code Style Rules
- Line length: 100 characters
- Use type hints for all public APIs
- Follow PEP 8 and PEP 257 for code style and docstrings
- Docstrings for all public functions/classes
- Use dataclasses for structured data
- Use Pydantic models for API schemas and validation

## Getting API Credentials

Before using the client, either for development or production, you'll need Apaleo API credentials:

### Register with Apaleo
1. Visit the [Apaleo Developer Portal](https://apaleo.dev)
2. Create a developer account or sign in
3. Navigate to "Apps" section

### Create an Application - Client Credentials Flow
1. Click "Connected apps" for client credentials flow
2. Click "Add a new app" then select "Add custom app"
3. Fill out the form

### Create an Application - Authorization Code Flow
1. Click "My store apps" for authorization code flow
2. Click "Add a new store app"
3. Fill out the form (name, description, redirect URI, secret, etc.)
4. Configure the app's permissions (scopes) based on your needs

### Get Your Credentials
After creating the application, you'll receive:
- **Client ID**: Public identifier for your application
- **Client Secret**: Private secret (keep secure!)
- **Redirect URI**: URL for authorization code flow (if applicable)

## Release Process

*(For maintainers)*

### Version Bumping

We use [semantic versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

```bash
# Update version via invoke task
inv increase-version --part minor  # or major, patch
```

### Release Checklist

- [ ] All tests pass across Python 3.10-3.13
- [ ] Documentation is up to date
- [ ] Version is bumped in pyproject.toml
- [ ] Git tag matches package version
- [ ] GitHub release is created
- [ ] Package is published to PyPI

## Advanced Contributing

### Performance Contributions

- Use `asyncio` profiling for async code
- Benchmark before/after changes
- Consider memory usage for large datasets
- Test with various network conditions

### Security Contributions

- Never log sensitive information (credentials, tokens)
- Use environment variables for test credentials
- Follow OWASP guidelines for HTTP clients
- Consider timing attacks in authentication

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>([scope]): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(core): add property search functionality

fix(auth): handle token refresh race condition

docs: update installation guide for Poetry users

test(integration): add tests for pagination edge cases
```

---

## Thank You!

Every contribution helps make Apaleo API Client better for everyone. Whether you're fixing a typo, adding a feature, or helping with documentation, your efforts are appreciated!

**Questions?** Don't hesitate to:
- [Open a discussion](https://github.com/lipppy/apaleo-api-client/discussions)
- [Ask in issues](https://github.com/lipppy/apaleo-api-client/issues)
- Reach out to the maintainers

Happy coding! 🚀
