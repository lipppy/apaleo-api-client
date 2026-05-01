"""Invoke tasks for development workflow."""

from invoke.context import Context
from invoke.tasks import task

# Variables

BASH_COLOR_YELLOW = "\033[93m"
BASH_COLOR_RED = "\033[91m"
BASH_COLOR_GREEN = "\033[92m"
BASH_COLOR_BLUE = "\033[94m"
BASH_COLOR_PURPLE = "\033[95m"
BASH_COLOR_END = "\033[0m"
BASH_INFO = f"{BASH_COLOR_BLUE}[INFO]{BASH_COLOR_END} "
BASH_WARNING = f"{BASH_COLOR_YELLOW}[WARNING]{BASH_COLOR_END} "
BASH_ERROR = f"{BASH_COLOR_RED}[ERROR]{BASH_COLOR_END} "
BASH_SUCCESS = f"{BASH_COLOR_GREEN}[SUCCESS]{BASH_COLOR_END} "


def confirm(prompt: str, default: bool = False) -> bool:
    """Prompt the user for a yes/no confirmation."""
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{prompt} {suffix} ").strip().lower()

    if not answer:
        return default

    return answer in ("y", "yes")


@task
def lint(c: Context) -> None:
    """Run linters."""
    c.run(f"echo '{BASH_INFO}Running linters...'")
    c.run("poetry run isort --check .")
    c.run("poetry run flake8 .")
    c.run("poetry run mypy --strict .")
    c.run(f"echo '{BASH_SUCCESS}Linters completed successfully.'")


@task
def format(c: Context, with_mypy: bool = False) -> None:
    """Format code using isort and ruff and run pre-commit hooks..."""
    c.run(f"echo '{BASH_INFO}Formatting code...'")
    c.run("poetry run isort .")
    c.run("poetry run ruff format .")
    c.run("poetry run pre-commit run --all-files")
    c.run("poetry run flake8 .")
    if with_mypy:
        c.run("poetry run mypy --strict .")
    c.run(f"echo '{BASH_SUCCESS}Code formatted successfully.'")


@task
def clean(c: Context) -> None:
    """Removing Python caches and temp files."""
    c.run(f"echo '{BASH_INFO}Cleaning Python bytecode and cache files...'")
    c.run("find ./ -name '*.py[cod]' -type f -delete")
    c.run("find . -type d -name '__pycache__' -exec rm -rf {} +")
    c.run("find . -type d -name '.pytest_cache' -exec rm -rf {} +")
    c.run("find . -type d -name '.mypy_cache' -exec rm -rf {} +")
    c.run("find . -type d -name '.ruff_cache' -exec rm -rf {} +")
    c.run("find . -type d -name '.tox' -exec rm -rf {} +")
    c.run("find . -type d -name '.nox' -exec rm -rf {} +")
    c.run("find . -type f -name '.coverage' -exec rm -f {} +")
    c.run(f"echo '{BASH_SUCCESS}Python caches and temp files cleaned.'")


@task()
def test(c: Context) -> None:
    """Run unit tests with coverage."""
    c.run(f"echo '{BASH_INFO}Running unit tests with coverage...'")
    c.run(
        "poetry run coverage run -m pytest -x -m unit && poetry run coverage report",
        pty=True,
    )
    c.run(f"echo '{BASH_SUCCESS}Unit tests completed successfully.'")


@task()
def test_integration(c: Context) -> None:
    """Run integration tests with coverage."""
    c.run(f"echo '{BASH_INFO}Running integration tests with coverage...'")
    c.run(
        "poetry run coverage run -m pytest -x -vv -s -m integration && poetry run coverage report",
        pty=True,
    )
    c.run(f"echo '{BASH_SUCCESS}Integration tests completed successfully.'")


@task
def test_nox(c: Context) -> None:
    """Run tests in nox sessions."""
    c.run(f"echo '{BASH_INFO}Running tests in nox sessions...'")
    c.run("poetry run nox -s tests", pty=True)
    c.run(f"echo '{BASH_SUCCESS}Tests completed successfully.'")


@task
def build(c: Context, clean: bool = False, verbose: bool = False) -> None:
    """Build the package using Poetry.

    Args:
        clean: Clean dist directory before building
        verbose: Enable verbose output
    """
    c.run(f"echo '{BASH_INFO}Building package...'")

    if clean:
        c.run(f"echo '{BASH_INFO}Cleaning dist directory...'")
        c.run("rm -rf dist/")

    build_cmd = "poetry build"
    if verbose:
        build_cmd += " --verbose"

    c.run(build_cmd)
    c.run(f"echo '{BASH_SUCCESS}Package built successfully.'")

    # Show built artifacts
    c.run(f"echo '{BASH_INFO}Built artifacts:'")
    c.run("ls -la dist/")


@task
def clean_build(c: Context, verbose: bool = False) -> None:
    """Clean the project and build the package."""
    c.run(f"echo '{BASH_INFO}Running clean build...'")
    clean(c)
    build(c, clean=True, verbose=verbose)


@task
def check(c: Context) -> None:
    """Run all quality checks (lint and test) before building."""
    c.run(f"echo '{BASH_INFO}Running quality checks...'")
    lint(c)
    test_nox(c)
    c.run(f"echo '{BASH_SUCCESS}All quality checks passed.'")


@task(pre=[check])
def build_checked(c: Context, verbose: bool = False) -> None:
    """Run quality checks and then build the package."""
    build(c, clean=True, verbose=verbose)


@task
def clean_docs(c: Context) -> None:
    """Clean generated documentation."""
    c.run(f"echo '{BASH_INFO}Cleaning generated documentation...'")
    c.run("rm -rf site/")
    c.run(f"echo '{BASH_SUCCESS}Generated documentation cleaned.'")


@task
def build_docs(c: Context) -> None:
    """Generate documentation using MkDocs."""
    c.run(f"echo '{BASH_INFO}Generating documentation...'")
    c.run("poetry run mkdocs build")
    c.run(f"echo '{BASH_SUCCESS}Documentation generated successfully.'")


@task
def serve_docs(c: Context) -> None:
    """Serve documentation locally using MkDocs."""
    c.run(f"echo '{BASH_INFO}Serving documentation locally...'")
    c.run("poetry run mkdocs serve --livereload", pty=True)
    c.run(f"echo '{BASH_SUCCESS}Documentation server stopped.'")


@task
def publish_docs(c: Context) -> None:
    """Publish documentation to GitHub Pages using MkDocs."""
    c.run(f"echo '{BASH_INFO}Publishing documentation to GitHub Pages...'")
    c.run("poetry run mkdocs gh-deploy --force")
    c.run(f"echo '{BASH_SUCCESS}Documentation published successfully.'")


@task
def docs(c: Context) -> None:
    """Build documentation and serve it locally."""
    clean_docs(c)
    build_docs(c)
    serve_docs(c)


@task
def increase_version(c: Context, part: str = "patch") -> None:
    """Increase the package version using Poetry.

    Args:
        part: Which part of the version to increase (major, minor, patch)
    """
    c.run(f"echo '{BASH_INFO}Increasing package version...'")
    c.run(f"poetry version {part}")
    c.run(f"echo '{BASH_INFO}New version: ' && poetry version --short")
    c.run("git add pyproject.toml")
    result = c.run("poetry version --short", hide=True)
    if result is None:
        c.run(f"echo '{BASH_ERROR}Failed to retrieve the new version.'")
        return
    version = result.stdout.strip()
    if confirm(f"Do you want to commit the version increase to git? (New version: {version})"):
        c.run(f"git commit -m 'chore(release): {version}'")
        c.run(f"echo '{BASH_SUCCESS}Package version increased successfully.'")


@task
def help(c: Context) -> None:
    """Display help information for tasks."""
    c.run(f"echo '{BASH_INFO}Available tasks:'")
    c.run("invoke --list")
    c.run(f"echo '{BASH_INFO}Use invoke <task> to run a specific task.'")
    c.run(
        f"echo '{BASH_INFO}For example: Run {BASH_COLOR_PURPLE}`invoke lint`{BASH_COLOR_END} to lint the code.'"  # NOQA: E501
    )
    c.run(f"echo '{BASH_INFO}For more information, check the documentation.'")
    c.run(f"echo '{BASH_INFO}Happy coding!'")
    c.run(f"echo '{BASH_SUCCESS}Help displayed successfully.'")
