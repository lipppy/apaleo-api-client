# Installation

Get started with Apaleo API Client quickly and easily. This type-safe, async SDK supports Python 3.10+ and can be installed using your preferred package manager.

## Package Installation

This library is published to PyPI. All installation methods below resolve the package from PyPI.

=== "poetry"

    ```bash
    poetry add apaleo-api-client
    ```

=== "pip"

    ```bash
    pip install apaleo-api-client
    ```

=== "uv"

    ```bash
    uv add apaleo-api-client
    ```

Core dependencies (automatically installed):

- [`httpx`](https://pypi.org/project/httpx/): A fully featured HTTP client for Python—powers our async operations.
- [`pydantic[email]`](https://pypi.org/project/pydantic/) (v2): Data validation and type safety using Python type annotations.
- [`dacite`](https://pypi.org/project/dacite/): Converts dictionaries to dataclasses for seamless type conversion.
- [`httpx-retries`](https://pypi.org/project/httpx-retries/): Automatic retry logic for robust API calls.
- [`polyfactory`](https://pypi.org/project/polyfactory/): Generates mock data for dry runs and testing.

If you've got Python 3.10+ and pip, uv, Poetry, or pipenv installed, you're good to go.

## Next Steps

Now that you have the library installed:

1. **[Learn the basics](why.md)** - Understand key concepts
2. **[Explore examples](../examples/index.md)** - See practical usage patterns
3. **[Read the API docs](../api/index.md)** - Dive into the full API reference
4. **[Join the community](contributing.md)** - Get help and contribute
