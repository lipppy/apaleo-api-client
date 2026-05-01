# Project Context

## Purpose

Apaleo API Client is a type-safe, async Python SDK for the Apaleo API.
It is built on httpx and Pydantic v2 and aims to provide modern, typed access to Apaleo domains, with primary focus on v1 APIs.

## Key Capabilities

- OAuth2 authentication support for client credentials and authorization code flows
- Async-first HTTP client with retries and concurrent pagination helpers
- Typed request/response models and domain-specific exceptions
- Documentation-first development with examples and API reference

## Current Shape

- Main package: `src/apaleoapi`
- Entry point: `ApaleoAPIClient` in `src/apaleoapi/client.py`
- API domains live under `src/apaleoapi/apaleo/`
- HTTP/auth layer lives under `src/apaleoapi/http/`
- Protocol/abstraction layer lives under `src/apaleoapi/ports/`
- Shared services live under `src/apaleoapi/services/`
- Tests are split into `tests/unit` and `tests/integration`

## API Coverage

- Core API: in progress
- Identity API: implemented
- Payment, Webhook, Integration, Fiscalization, Profile: planned or partial scaffolding exists

## Development Workflow

- Use Poetry for dependency and environment management
- Preferred local Python for development is 3.12
- Common tasks are run via Invoke
- Typical commands:
	- `poetry install --with dev,test,lint,docs`
	- `poetry run invoke test`
	- `poetry run invoke lint`
	- `poetry run invoke format`

## Quality Expectations

- Keep public APIs typed and mypy compliant
- Follow existing adapter/transport/service patterns
- Prefer minimal, focused changes over broad refactors
- Preserve async behavior and typed models
- Update docs/examples when behavior or public usage changes

## Useful Context For Agents

- This repo is both a library and its documentation site
- Docs in `docs/` are part of the product and should stay aligned with code
- Integration tests use real Apaleo credentials and make real API calls
- Dry-run support exists and is useful for testing client behavior without live requests
