# tests

## Responsibility

This directory contains the complete automated test suite for Hydra Runtime. Tests are written using pytest and organized to mirror the source directory structure exactly. Every module in `hydra/` has a corresponding test file in `tests/`.

---

## Rules for This Directory

- Test files are named `test_<module_name>.py`.
- Test functions are named `test_<function_name>_<scenario_description>`.
- Tests must be independent. No test should depend on the output or side effects of another test.
- External dependencies (HTTP calls, database writes, filesystem writes) must be mocked. Tests must not make real network requests or leave artifacts on disk.
- Use pytest fixtures for all shared setup and teardown. Do not use class-based test setup.
- Integration tests that test interactions between two or more modules are welcome but must be clearly separated from unit tests using a `tests/integration/` subdirectory.
- The CI pipeline runs the full test suite using `uv run pytest`. All tests must pass before any pull request can be merged.

---

## Directory Structure

The test directory mirrors the source structure:

```
tests/
  __init__.py
  conftest.py                          Shared fixtures used across all tests
  runtime/
    providers/
      test_base.py
      test_ollama.py
    router/
      test_router.py
    compiler/
      test_compiler.py
    workspace/
      test_analyzer.py
    memory/
      test_store.py
    graph/
      test_graph.py
    plugins/
      test_base.py
    checkpoints/
      test_manager.py
    state/
      test_state.py
    session/
      test_session.py
  database/
    test_db.py
    test_models.py
  models/
    test_schemas.py
  utils/
    test_helpers.py
  config/
    test_config.py
  commands/
    test_init.py
    test_ask.py
    test_status.py
```

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package so pytest can discover tests correctly.

### conftest.py

**Purpose**: Defines shared pytest fixtures available to all test files without importing.

**What this file must contain**:

- A `db_session` fixture that creates an in-memory SQLite database and returns a session for use in tests. The database is torn down after each test.
- A `sample_settings` fixture that returns a `Settings` instance with safe test defaults.
- A `mock_provider` fixture that returns a mock implementation of `BaseProvider` that returns predefined responses.
- A `sample_memory_node` fixture that returns a pre-built `MemoryNode` Pydantic model for use in memory tests.
- A `tmp_workspace` fixture that creates a temporary directory structure simulating a Python project and tears it down after the test.
