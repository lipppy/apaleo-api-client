import importlib.metadata


def version_info() -> str:
    """Returns the version information of the Apaleo API Client."""
    version = importlib.metadata.version("apaleo-api-client")
    return version
