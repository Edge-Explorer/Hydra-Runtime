# Contributing to Hydra Runtime

Thank you for your interest in contributing to Hydra Runtime. This document outlines the process, standards, and expectations for contributors. Please read it carefully before opening an issue or submitting a pull request.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Branching Strategy](#branching-strategy)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

This project is maintained with the expectation that all contributors treat each other with respect. Harassment, discrimination, or disruptive behavior of any kind will not be tolerated. If you witness or experience any such behavior, please report it by opening a private issue or contacting the maintainer directly.

---

## How to Contribute

There are several ways to contribute to Hydra Runtime:

- Fixing bugs reported in the issue tracker
- Implementing features listed in open issues
- Writing or improving documentation
- Adding tests for untested code paths
- Reviewing open pull requests
- Reporting new bugs or edge cases
- Suggesting architectural improvements

If you are new to the project, look for issues labeled `good first issue`. These are scoped to be approachable without deep familiarity with the entire codebase.

Before starting work on a non-trivial change, open an issue describing what you plan to do. This prevents duplicate effort and ensures your contribution aligns with the project roadmap.

---

## Development Setup

### Prerequisites

- Python 3.12 or higher
- uv (Python package and environment manager)
- Git
- Ollama installed locally for provider testing (optional but recommended)

### Steps

```bash
# Clone the repository
git clone https://github.com/Edge-Explorer/Hydra-Runtime.git
cd Hydra-Runtime

# Create the virtual environment
uv venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (Linux / macOS)
source .venv/bin/activate

# Install all dependencies including development tools
uv sync --all-extras

# Verify the setup by running the test suite
uv run pytest
```

---

## Project Structure

Understanding the layout of the project is important before contributing. Each directory has a specific responsibility and strict rules about what kind of code belongs in it.

```
hydra/
  cli/              Entry point for the Typer CLI application
  commands/         One file per CLI command group, thin handlers only
  runtime/          Core runtime logic, the intelligence of the system
    providers/      Abstract provider interface and concrete implementations
    router/         Model selection and routing logic
    compiler/       Context compilation and prompt assembly
    workspace/      Project scanning and DNA generation
    memory/         Vector memory store and embedding management
    graph/          Knowledge graph construction and traversal
    plugins/        Plugin interface and built-in plugin implementations
    checkpoints/    Session state snapshotting and restoration
    state/          Live session state management
    session/        Multi-workspace session lifecycle management
  database/         SQLAlchemy engine, ORM models, and migration setup
  models/           Pydantic data schemas shared across modules
  utils/            Shared utility functions with no business logic
  config/           Configuration loading, validation, and persistence
tests/              Pytest test suite mirroring the source structure
```

Detailed documentation for each directory is available in the README.md file within that directory.

---

## Branching Strategy

The `main` branch is the stable branch. Direct pushes to `main` are restricted. All changes must go through a pull request.

Use the following branch naming convention:

| Type        | Pattern                         | Example                            |
|-------------|---------------------------------|------------------------------------|
| Feature     | `feat/<short-description>`      | `feat/ollama-provider`             |
| Bug fix     | `fix/<short-description>`       | `fix/config-load-fallback`         |
| Docs        | `docs/<short-description>`      | `docs/update-contributing`         |
| Refactor    | `refactor/<short-description>`  | `refactor/compiler-token-budget`   |
| Tests       | `test/<short-description>`      | `test/memory-store-unit`           |
| CI/Tooling  | `ci/<short-description>`        | `ci/add-mypy-check`                |

---

## Commit Message Convention

This project follows the Conventional Commits specification. Every commit message must follow this format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type       | When to use                                              |
|------------|----------------------------------------------------------|
| `feat`     | A new feature or capability                              |
| `fix`      | A bug fix                                                |
| `docs`     | Documentation changes only                              |
| `style`    | Formatting changes, no logic changes (black, isort)     |
| `refactor` | Code restructuring with no feature or bug change        |
| `test`     | Adding or modifying tests                               |
| `ci`       | Changes to CI/CD configuration                          |
| `chore`    | Dependency updates, build changes, minor maintenance    |

### Scope

The scope is the module or area of the codebase being changed. Examples: `config`, `providers`, `compiler`, `memory`, `cli`, `router`.

### Examples

```
feat(providers): add Ollama streaming response support

fix(config): handle missing runtime.yaml with default fallback

docs(contributing): add branching strategy section

test(memory): add unit tests for vector similarity search

style(compiler): apply black formatting
```

---

## Pull Request Process

1. Create a branch from `main` following the naming convention above.
2. Make your changes, keeping commits focused and atomic.
3. Ensure all tests pass locally by running `uv run pytest`.
4. Ensure formatting passes by running `uv run black hydra tests` and `uv run isort hydra tests`.
5. Push your branch and open a pull request against `main`.
6. Fill in the pull request template completely.
7. Reference any related issues using `Closes #<issue-number>` in the PR description.
8. Wait for the CI pipeline to pass. A pull request with a failing CI will not be reviewed.
9. Address any review comments and push updates to the same branch.
10. A maintainer will merge the pull request once it is approved.

### Pull Request Template

When opening a pull request, include the following in the description:

```
## Summary
A brief description of what this PR changes and why.

## Changes
- List of specific changes made

## Related Issues
Closes #<issue-number>

## Testing
Describe how you tested the changes.

## Checklist
- [ ] Tests pass locally
- [ ] Black and isort formatting checks pass
- [ ] New code has corresponding tests
- [ ] Documentation updated if applicable
```

---

## Code Style

This project enforces consistent code style using the following tools:

**Black**: Code formatter. Black is run with default settings. Do not configure line length or other options unless agreed upon by maintainers.

**isort**: Import sorter. Imports must be sorted in the order: standard library, third-party, local. isort is run with default settings compatible with Black.

**mypy**: Static type checker. All new code must include type annotations. mypy will be enforced as the project matures.

Before committing, always run:

```bash
uv run black hydra tests
uv run isort hydra tests
```

### Additional Style Rules

- All functions and methods must have docstrings describing their purpose, parameters, and return values.
- All module-level files must have a module docstring at the top describing the module's responsibility.
- No magic numbers. Constants must be defined at the module level with descriptive names.
- No wildcard imports. Every import must be explicit.
- Abstract base classes must be used for all swappable interfaces (providers, memory stores, plugins).
- No business logic in CLI command handlers. Handlers call runtime modules and render output only.
- No database calls outside of `hydra/database/` and `hydra/runtime/` modules.
- No direct HTTP calls outside of `hydra/runtime/providers/`.

---

## Testing Requirements

Every non-trivial contribution must include tests. The following rules apply:

- Tests live in the `tests/` directory and mirror the source structure. A test for `hydra/runtime/memory/store.py` goes in `tests/runtime/memory/test_store.py`.
- Test files are named `test_<module_name>.py`.
- Test functions are named `test_<function_name>_<scenario>`.
- Use pytest fixtures for setup and teardown.
- Use `unittest.mock` or `pytest-mock` to mock external dependencies such as HTTP calls and database connections.
- Aim for unit tests that test individual functions in isolation. Integration tests that test module interactions are welcome in addition to unit tests but are not a substitute.
- The CI pipeline runs `uv run pytest` and must pass before any PR is merged.

---

## Issue Reporting

When reporting a bug, please include the following:

- A clear and concise description of the problem
- The exact command you ran or action you took
- The full error message and traceback if applicable
- Your operating system and Python version
- The output of `hydra --version` if applicable
- Steps to reproduce the issue reliably

Use the bug report issue template when available.

---

## Feature Requests

When requesting a feature, please include:

- A description of the problem you are trying to solve
- A description of your proposed solution
- An explanation of why this feature belongs in the core runtime as opposed to a plugin
- Any examples of similar functionality in other tools

Feature requests will be evaluated based on alignment with the project roadmap, implementation complexity, and community interest.

---

## Questions

If you have a question that is not answered by the documentation, open a discussion in the GitHub Discussions tab rather than an issue. Issues are reserved for confirmed bugs and accepted feature requests.
