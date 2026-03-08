# Contributing to Apaleo API Client

We welcome contributions to the Apaleo API Client! Whether you're fixing bugs, adding features, improving documentation, or helping with testing, your contributions are valued.

## 🚀 **Quick Start for Contributors**

### **1. Set Up Development Environment**

```bash
# Fork the repository on GitHub first, then clone
git clone https://github.com/<your-username>/apaleo-api-client.git
cd apaleo-api-client

# Install with all development dependencies
poetry install --with dev,test,lint,docs

# Activate the virtual environment
poetry shell

# Verify installation
inv help
```

### **2. Check Everything Works**

```bash
# Run tests
inv test

# Run linting
inv lint

# Format code
inv format

# Build documentation
inv docs
```

### **3. Make Your Changes**

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Run tests and linting
inv test
inv lint

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### **4. Submit a Pull Request**

1. Go to the GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Wait for review feedback

## 📄 **Project Structure**

 Understanding the codebase structure:

```
src/apaleoapi/
├── __init__.py                # Package exports
├── client.py                  # Main ApaleoAPIClient
├── constants.py               # API endpoints and constants
├── exceptions.py              # Custom exception classes
├── logging.py                 # Logging configuration
├── schemas.py                 # Pydantic schema definitions
├── typing.py                  # Type definitions
│
├── apaleo/                    # API domain modules
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
└── services/                  # Support services
    ├── list_fetcher.py        # Pagination handling
    ├── response_handler.py    # Response processing
    └── response_validator.py  # Response validation
```

## 🗺️ **Development Workflow**

### **Available Tasks (via invoke)**

```bash
inv help                 # Show all available tasks

# Development
inv test                 # Run tests with pytest
inv test-nox             # Test across Python 3.10-3.13

# Code Quality
inv lint                 # Run all linters (ruff, mypy, etc.)
inv format               # Format code (ruff format, isort)
inv check                # Check code quality without fixing

# Documentation
inv docs                 # Build and serve documentation
inv docs-build           # Build documentation only
inv docs-clean           # Clean generated docs

# Building
inv build                # Build package
inv clean                # Clean build artifacts
```

### **Code Style**

We use these tools for code quality:

- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **isort**: Import sorting
- **pytest**: Testing framework

#### **Code Style Rules**
- Line length: 100 characters
- Use type hints for all public APIs
- Follow PEP 8 and Black formatting
- Docstrings for all public functions/classes
- Use dataclasses for structured data

## 📅 **Release Process**

*(For maintainers)*

### **Version Bumping**

We use [semantic versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

```bash
# Update version in pyproject.toml
poetry version patch|minor|major

# Update CHANGELOG.md
# Git commit and tag
git add .
git commit -m "chore: bump version to vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

### **Release Checklist**

- [ ] All tests pass across Python 3.10-3.13
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version is bumped in pyproject.toml
- [ ] Git tag matches package version
- [ ] GitHub release is created
- [ ] Package is published to PyPI

## 🚀 **Advanced Contributing**

### **Performance Contributions**

- Use `asyncio` profiling for async code
- Benchmark before/after changes
- Consider memory usage for large datasets
- Test with various network conditions

### **Security Contributions**

- Never log sensitive information (credentials, tokens)
- Use environment variables for test credentials
- Follow OWASP guidelines for HTTP clients
- Consider timing attacks in authentication

### **API Design Principles**

- Favor async methods for I/O operations
- Use type hints for all public APIs
- Make required parameters explicit
- Provide sensible defaults for optional parameters
- Use dataclasses for complex parameters
- Handle errors gracefully with typed exceptions

## 📉 **Commit Message Format**

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

## 💙 **Thank You!**

Every contribution helps make Apaleo API Client better for everyone. Whether you're fixing a typo, adding a feature, or helping with documentation, your efforts are appreciated!

**Questions?** Don't hesitate to:
- [Open a discussion](https://github.com/lipppy/apaleo-api-client/discussions)
- [Ask in issues](https://github.com/lipppy/apaleo-api-client/issues)
- Reach out to the maintainers

Happy coding! 🚀
