---
name: test-unit
description: Create or update unit tests following this repo's conventions
argument-hint: "Specify the file, symbol, or behavior to cover"
---

Create or update unit tests for the requested file, symbol, or behavior.
Work in this repository's existing style and prefer minimal, focused changes over broad rewrites.

Rules:
- Use `pytest` and match existing tests under `tests/unit/`.
- Add `pytestmark = [pytest.mark.unit]` when creating a new unit test file.
- Prefer `unittest.mock` (`Mock`, `AsyncMock`, `patch`) for external dependencies.
- Keep tests isolated from network, filesystem, environment, and real credentials.
- Follow Arrange-Act-Assert and use descriptive test names.
- Parametrize only when it improves clarity and reduces repetition.
- Reuse existing fixtures from `tests/unit/conftest.py` when appropriate.
- Cover the requested behavior first, then add only the most relevant edge cases.
- If a test file does not exist, create it in the matching location under `tests/unit/` using the repo naming pattern `test_<module>.py`.
- Do not create `__init__.py` files in `tests/`.
- Keep assertions specific and behavior-focused.
- After editing tests, validate with `poetry run invoke test` and ensure the result remains mypy compliant with `poetry run invoke lint` when your changes affect typing.
- Do not add integration tests unless the request explicitly asks for them.
- If the request is ambiguous, ask only the single most necessary clarifying question.

Request:
{{input}}