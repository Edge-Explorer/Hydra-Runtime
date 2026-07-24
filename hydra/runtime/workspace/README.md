# hydra/runtime/workspace

## Responsibility

This directory contains the workspace analyzer, which scans a project directory and extracts structured information about the project. This information is stored as the Project DNA and is used by the context compiler to give the model an accurate understanding of the codebase before every interaction.

---

## Rules for This Directory

- The workspace analyzer is the only module permitted to perform filesystem scanning.
- The analyzer must not make network calls or database queries.
- Project DNA must be serialized to a local `.hydra/dna.json` file in the workspace directory.
- The analyzer must handle missing or unrecognizable project structures gracefully without raising exceptions.
- Detection heuristics must be additive. The analyzer improves its confidence as it finds more signal files, rather than failing if a particular file is absent.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### analyzer.py

**Purpose**: Implements the `WorkspaceAnalyzer` class that scans a project directory and builds the `ProjectDNA` model.

**What this file must contain**:

- The `WorkspaceAnalyzer` class initialized with the workspace directory path.
- A `scan() -> ProjectDNA` method that performs the full analysis pipeline.
- The analysis pipeline detects:
  - **Primary language**: inferred from file extensions, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc.
  - **Framework**: inferred from dependency manifests (FastAPI, Django, Express, React, etc.).
  - **Package manager**: detected from lockfiles (`uv.lock`, `package-lock.json`, `Cargo.lock`, etc.).
  - **Entry points**: detected from common patterns (`main.py`, `index.ts`, `app.py`, `cmd/`, etc.).
  - **Database**: inferred from dependencies (`sqlalchemy`, `prisma`, `mongoose`, etc.).
  - **Architecture indicators**: presence of `docker-compose.yml`, `kubernetes/`, `Makefile`, `CI` configuration, etc.
  - **Test framework**: detected from `pytest`, `jest`, `cargo test` setup.
  - **Documentation**: presence of `docs/`, `README.md`, docstring density estimate.
- A `save(dna: ProjectDNA)` method that serializes the DNA to `.hydra/dna.json`.
- A `load() -> ProjectDNA` method that reads a previously saved DNA file.
- A `refresh() -> ProjectDNA` method that re-runs the scan and updates the saved DNA.

**What this file must not contain**:
- Database access.
- Network calls.
- Prompt construction.
- Any logic unrelated to filesystem inspection and project detection.
