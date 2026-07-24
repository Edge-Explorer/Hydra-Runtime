# Hydra Runtime

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Edge-Explorer/Hydra-Runtime/actions/workflows/ci.yml/badge.svg)](https://github.com/Edge-Explorer/Hydra-Runtime/actions/workflows/ci.yml)

---

## What is Hydra Runtime

Hydra Runtime is an open-source AI orchestration runtime built for developers who work with multiple large language models across multiple projects. It is not a chatbot wrapper or a prompt manager. It is a runtime layer that sits between the developer and the AI model, managing memory, context, workspace intelligence, session state, and model routing independently of any specific LLM.

The core problem Hydra solves: every time a developer switches models, starts a new session, or moves between projects, all context is lost. The model has no knowledge of what decisions were made, what constraints exist, what the codebase looks like, or what tasks are in progress. Hydra eliminates this problem by maintaining persistent, structured memory and building optimized context payloads before every model interaction.

The LLM in Hydra is treated as a plugin. The runtime handles everything else.

---

## Core Principles

**Local first**: All data is stored locally by default using SQLite and FAISS. No cloud dependency is required to run the project. The storage layer is interface-driven, meaning cloud-backed implementations can be added without changing the core runtime.

**Interface driven**: Every major module communicates through a well-defined abstract base class. The router, memory store, provider, compiler, and plugin system are all independently swappable. No module should depend on the internal implementation of another.

**No framework lock-in**: Hydra does not use LangChain, LlamaIndex, or any AI orchestration framework internally. All orchestration logic is written in plain Python using focused libraries. This keeps the architecture transparent, lightweight, and easier to extend.

**Incremental releases**: The project is built phase by phase, with each phase producing working, testable functionality before the next begins.

---

## What Hydra Does

### Context Compilation

When a developer runs a query such as `hydra ask "fix the authentication middleware"`, the model does not receive just that sentence. Hydra compiles a structured context payload that includes the current git branch, a diff of recently modified files, semantically relevant memory nodes retrieved from the local vector database, the project DNA (language, framework, dependencies, architecture), any active task or goal, and relevant prior decisions. This compiled payload is what gets sent to the model.

### Workspace Intelligence

When a workspace is initialized using `hydra init`, Hydra scans the project directory for signals such as `pyproject.toml`, `package.json`, `requirements.txt`, `Dockerfile`, `README.md`, `.git`, and source directories. From these it builds a Project DNA document that describes the language, framework, architecture style, dependencies, entry points, and database setup. This DNA is stored locally and used in every subsequent context compilation step.

### Memory Graph

Instead of storing conversation history as a linear message log, Hydra stores information as typed nodes connected by typed edges. Node types include Decision, Task, Bug, File, Class, Function, API, and Constraint. Edge types include depends_on, implements, references, fixes, and modifies. This structure allows the runtime to retrieve deeply relevant context for a query rather than just returning recent messages.

### Model Routing

The router receives the intent of a query and selects the most appropriate model provider based on capability rules. Coding tasks are routed to code-specialized models. Reasoning-heavy tasks are routed to larger models. Low-priority tasks are routed to faster, cheaper models. The routing logic is rule-based initially and can be extended to use ML-based scoring later.

### Session and State Management

Hydra maintains an active session per workspace. The session stores the current goal, active tasks, current model, recent files, active constraints, git branch, and workspace directory. This state persists across terminal sessions so the model always has access to what was happening the last time the developer was working.

### Checkpoint and Rollback

Hydra allows the developer to create named checkpoints of the current session state. These checkpoints can be listed, restored, or branched. This is analogous to git commits but for AI session context rather than source code.

### Plugin System

Hydra exposes a plugin interface that allows external tools to be connected to the runtime. Built-in plugins will include Git, filesystem, and terminal. External plugins for GitHub, Docker, Jira, Notion, and MCP-compatible tools can be added by contributors without modifying the core runtime.

---

## High Level Architecture

```
                       CLI (Typer)
                            |
                   Command Dispatcher
                            |
         -------------------|-----------------
         |                  |                |
      Router           Workspace          Memory
         |                  |                |
    Providers          Project DNA     Knowledge Graph
         |                  |                |
         -------------------|-----------------
                            |
                   Context Compiler
                            |
                     Selected Model
```

---

## Tech Stack

| Purpose              | Library                                      |
|----------------------|----------------------------------------------|
| CLI framework        | typer                                        |
| Terminal UI          | rich                                         |
| Configuration        | pydantic, pydantic-settings, pyyaml          |
| Database ORM         | sqlalchemy 2.0, alembic                      |
| Vector search        | faiss-cpu                                    |
| Embeddings           | sentence-transformers (BAAI/bge-small-en-v1.5) |
| Graph representation | networkx                                     |
| Git integration      | gitpython                                    |
| HTTP clients         | httpx                                        |
| Serialization        | orjson                                       |
| Testing              | pytest                                       |
| Formatting           | black, isort                                 |
| Type checking        | mypy                                         |

---

## Project Structure

The following describes every directory and file in the project, what it is responsible for, what kind of code belongs in it, and why it was created as a separate module.

---

### hydra/

This is the root Python package for the entire runtime. All source code lives under this directory. The `__init__.py` at this level keeps it minimal and should not import anything from submodules directly.

---

### hydra/cli/

**Purpose**: Entry point for the command line interface.

**What belongs here**: The Typer application instance is created here. Shell completion setup and top-level application metadata belong here. This file registers all subcommand groups by importing them from `hydra/commands/`. It should not contain business logic of any kind.

**Why separate**: The CLI layer is only responsible for parsing user input and delegating to the appropriate command handler. Mixing business logic into the CLI makes it impossible to test commands without simulating terminal input.

#### hydra/cli/main.py
Creates the Typer app instance. Imports and registers all command modules from `hydra/commands/`. Defines the application name, version flag, and help text. This file is the entry point defined in `pyproject.toml` under `[project.scripts]`.

---

### hydra/commands/

**Purpose**: Contains one file per CLI command group. Each file defines what happens when a specific command is invoked.

**What belongs here**: Command handler functions decorated with `@app.command()`. Each handler should validate input, call the appropriate runtime module, and use Rich to render the output. No SQL queries, no embedding logic, no HTTP calls should appear directly in these files.

**Why separate**: Commands are the interface between the user and the runtime. Keeping them thin and delegating all logic to the runtime modules makes each command testable in isolation and keeps the CLI layer clean.

#### hydra/commands/init.py
Handles the `hydra init` command. Calls the workspace analyzer to scan the current directory, initializes the database, creates the default configuration file, and sets up the initial session. Renders a summary of what was detected using Rich panels.

#### hydra/commands/ask.py
Handles the `hydra ask` command. Accepts a user query as a string argument. Calls the context compiler to build the prompt payload, passes it to the router to select a provider, streams or prints the model response using Rich markdown rendering.

#### hydra/commands/switch.py
Handles the `hydra switch` command. Allows the developer to change the active model or provider. Updates the session state and configuration. Lists available models using Rich tables.

#### hydra/commands/memory.py
Handles the `hydra memory` command group. Subcommands include listing memory nodes, searching memory by keyword, deleting specific nodes, and displaying the knowledge graph structure.

#### hydra/commands/status.py
Handles the `hydra status` command. Reads the current session state and renders an overview including the active model, current workspace, active tasks, open goals, current git branch, and memory node count.

#### hydra/commands/config.py
Handles the `hydra config` command group. Subcommands include getting and setting configuration values, displaying the full current configuration, and resetting to defaults.

---

### hydra/runtime/

**Purpose**: The core of the entire project. Contains all the intelligence of the runtime. Nothing in this package should import from `hydra/cli/` or `hydra/commands/`.

**Why separate**: The runtime is the reusable brain of Hydra. By keeping it completely decoupled from the CLI, the same runtime can be used by a future web interface, API server, or Python SDK without modification.

---

### hydra/runtime/providers/

**Purpose**: Abstracts all communication with AI model providers behind a single interface.

**What belongs here**: The abstract base class that all providers must implement. Concrete provider implementations for each supported service. A provider registry that maps provider names to their classes.

**Why separate**: The rest of the runtime should never know which model it is talking to. The compiler sends a structured payload to a provider and gets back a string. Whether that string came from Ollama, Gemini, or OpenAI is irrelevant to the compiler, the router, or the memory system.

#### hydra/runtime/providers/base.py
Defines the `BaseProvider` abstract class. Declares the `generate` and `generate_stream` abstract methods that every provider must implement. Defines the standard request and response structures as Pydantic models. Nothing in this file should make network calls or reference a specific model vendor.

#### hydra/runtime/providers/ollama.py
Implements `BaseProvider` for the Ollama local inference server. Uses `httpx` to call the Ollama REST API. Implements both full response and streaming response modes. Contains only Ollama-specific logic such as endpoint paths, request format, and response parsing.

---

### hydra/runtime/router/

**Purpose**: Decides which provider and model to use for a given query.

**What belongs here**: The routing logic that evaluates a query's intent and maps it to the most appropriate provider. Capability tables that define which models are suited for which task types. Later, ML-based routing scoring can be added here.

**Why separate**: Routing is a distinct concern from compilation and from provider communication. The router takes a query intent and session context as input and returns a provider name and model name. It does not know how to call the provider and it does not know how to build a prompt.

#### hydra/runtime/router/router.py
Implements the `ModelRouter` class. Contains a rule-based routing function that classifies the query intent (coding, reasoning, vision, general) and returns the appropriate provider and model identifier from the active configuration. References the session state to respect any manually pinned model.

---

### hydra/runtime/compiler/

**Purpose**: Builds the complete prompt payload that gets sent to the model.

**What belongs here**: The logic that assembles all available context sources into a single structured prompt. Token budgeting logic that ensures the compiled prompt stays within the model's context window. Retrieval calls to the memory store and workspace analyzer.

**Why separate**: Prompt engineering is a complex, evolving concern. The compiler centralizes all decisions about what context to include, in what order, and at what level of detail. No other module should be building or modifying prompts.

#### hydra/runtime/compiler/compiler.py
Implements the `ContextCompiler` class. The `compile` method accepts the user query and current session state. It queries the memory store for semantically similar nodes, reads the project DNA, fetches the current git diff, and assembles a system prompt and user prompt. It applies token budget limits and compresses context if necessary before returning the final payload.

---

### hydra/runtime/workspace/

**Purpose**: Understands the developer's project by scanning the workspace directory.

**What belongs here**: File system scanning logic. Heuristics for detecting programming language, framework, package manager, database, and entry point. Logic for reading README files and parsing dependency manifests. The serialization of Project DNA to a local JSON file.

**Why separate**: Workspace intelligence is a discrete capability. The analyzer runs once during initialization and can be run again to refresh the DNA when the project changes. The compiler and memory system consume its output but should not contain any file scanning logic themselves.

#### hydra/runtime/workspace/analyzer.py
Implements the `WorkspaceAnalyzer` class. The `scan` method walks the workspace directory, reads key files, and builds a `ProjectDNA` Pydantic model containing detected language, framework, dependencies, architecture indicators, entry points, and database type. Saves the result to a local `.hydra/dna.json` file.

---

### hydra/runtime/memory/

**Purpose**: Provides persistent, semantically searchable memory for the runtime.

**What belongs here**: The abstract `BaseMemoryStore` interface. The SQLite-backed implementation that stores memory nodes and their vector embeddings. FAISS index management for similarity search. The embedding generation pipeline using sentence-transformers.

**Why separate**: Memory retrieval is a specialized concern involving embeddings, vector search, and graph traversal. Mixing this into the compiler or the database module would create tight coupling that makes it impossible to swap the memory backend later.

#### hydra/runtime/memory/store.py
Implements the `MemoryStore` class. Provides methods to add a memory node (with automatic embedding generation), search for similar nodes given a query string, retrieve nodes by type, and delete nodes by ID. Manages the FAISS index lifecycle including saving and loading from disk between sessions.

---

### hydra/runtime/graph/

**Purpose**: Manages the knowledge graph that represents relationships between memory nodes.

**What belongs here**: Graph construction and traversal logic using networkx. Methods for adding nodes and typed edges to the in-memory graph. Serialization of the graph structure to the SQLite database. Query methods for finding related nodes given a starting node.

**Why separate**: The graph layer is distinct from the vector memory layer. The memory store handles semantic similarity search. The graph layer handles structural relationships. Together they provide a complete picture of what the runtime knows, but they serve different retrieval strategies.

#### hydra/runtime/graph/graph.py
Implements the `KnowledgeGraph` class. Maintains a directed networkx graph in memory. Provides methods to add nodes of typed categories, add directional edges with relationship labels, traverse from a node to find related nodes within a depth limit, and export the graph to a format that can be rendered in the terminal.

---

### hydra/runtime/plugins/

**Purpose**: Defines the plugin interface and hosts built-in plugin implementations.

**What belongs here**: The abstract `BasePlugin` class that all plugins must implement. Built-in plugins for Git, filesystem, and terminal. A plugin loader that discovers and registers available plugins at runtime startup.

**Why separate**: Plugins extend the runtime's capabilities without requiring changes to core modules. By defining a clean plugin interface here, third-party contributors can build and distribute plugins as separate Python packages that Hydra can load automatically.

#### hydra/runtime/plugins/base.py
Defines the `BasePlugin` abstract class. Declares methods that all plugins must implement including `name`, `description`, `initialize`, and `execute`. Defines the standard input and output structures for plugin execution. Does not implement any plugin-specific logic.

---

### hydra/runtime/checkpoints/

**Purpose**: Manages the creation, listing, restoration, and branching of session state checkpoints.

**What belongs here**: Logic for serializing the current session state to a named checkpoint record in the database. Logic for restoring a session from a checkpoint. The checkpoint history viewer.

**Why separate**: Checkpointing is an operational concern separate from session management. The session manager tracks the live state. The checkpoint manager handles the historical snapshots of that state.

#### hydra/runtime/checkpoints/manager.py
Implements the `CheckpointManager` class. Provides methods to create a checkpoint from the current session state, list all checkpoints for a workspace, restore a session state from a named checkpoint, and delete checkpoints by name or age.

---

### hydra/runtime/state/

**Purpose**: Manages the live runtime state for the current session.

**What belongs here**: The `StateManager` class that reads and writes the active session's goal, open tasks, current model, current branch, recent files, and constraints. Persistence of state between terminal sessions using the SQLite database.

**Why separate**: State management is a read-heavy, write-light concern that many modules need access to. Centralizing it here prevents circular dependencies and ensures all modules read from and write to a single source of truth.

#### hydra/runtime/state/state.py
Implements the `StateManager` class. Loads the current session state from the database on startup. Provides getter and setter methods for every state field. Persists state changes to the database after every write. Provides a method to reset the state to defaults.

---

### hydra/runtime/session/

**Purpose**: Manages workspace sessions, allowing multiple projects to have independent state and memory.

**What belongs here**: Logic for creating a new session for a workspace, switching between sessions, listing all available sessions, and archiving or deleting sessions.

**Why separate**: A developer may work across multiple projects, each needing independent state, memory, and DNA. The session layer isolates these concerns so that asking a question in one project's session does not pollute another project's memory or context.

#### hydra/runtime/session/session.py
Implements the `SessionManager` class. Associates each session with a workspace directory path. Creates new session records in the database. Provides methods to activate a session, list all sessions, retrieve the currently active session, and delete a session along with its associated memory and checkpoints.

---

### hydra/database/

**Purpose**: Manages all SQLite database interactions including schema definition, connection lifecycle, and migrations.

**What belongs here**: The SQLAlchemy engine and session factory. The declarative base class used by all ORM models. Alembic migration configuration. No business logic of any kind belongs in this directory. It is purely infrastructure.

**Why separate**: Database infrastructure is a low-level concern. If the storage backend changes from SQLite to PostgreSQL in the future, only this directory should need to change. Runtime modules should never create database connections directly.

#### hydra/database/db.py
Creates the SQLAlchemy engine using the database URL from the configuration. Defines the `SessionLocal` session factory. Defines the `Base` declarative class that all ORM models inherit from. Provides a `get_db` context manager for obtaining database sessions in other modules.

#### hydra/database/models.py
Defines all SQLAlchemy ORM table models including Session, MemoryNode, MemoryEdge, Checkpoint, and ProjectDNA. Each model class maps directly to a database table. No business logic or queries belong in this file, only table structure definitions.

---

### hydra/models/

**Purpose**: Contains all Pydantic data schemas used across the project for data validation, serialization, and type safety.

**What belongs here**: Pydantic models that represent the data structures passed between modules. These are not database models. They are the data contracts that modules use when communicating with each other. Provider request and response schemas, memory node schemas, session state schemas, and context compiler output schemas all belong here.

**Why separate**: Pydantic schemas define the contracts between modules. If every module defines its own internal data structures, they become tightly coupled and refactoring becomes extremely difficult. Centralizing schemas here ensures consistency.

#### hydra/models/schemas.py
Defines all Pydantic BaseModel classes used by the runtime. Examples include `ProviderRequest`, `ProviderResponse`, `MemoryNode`, `ProjectDNA`, `SessionState`, `Checkpoint`, `ContextPayload`, and `RouterDecision`. These models are imported by runtime modules as needed.

---

### hydra/utils/

**Purpose**: Shared utility functions that are used by multiple modules but do not belong to any specific module.

**What belongs here**: Token counting helpers, text truncation utilities, file reading helpers, logging configuration, and other small functions that multiple modules need. No business logic, no database calls, and no model-specific code belongs here.

**Why separate**: Utility functions that appear in multiple places should live in one place to avoid duplication. However, they must not contain any logic that belongs to a specific module.

#### hydra/utils/helpers.py
Contains utility functions such as token estimation given a string and a model name, text truncation to a maximum token count, safe file reading with encoding detection, timestamp formatting, and path normalization across operating systems.

---

### hydra/config/

**Purpose**: Manages loading, validating, and saving the runtime configuration from the `runtime.yaml` file.

**What belongs here**: The Pydantic Settings models that define the structure of the configuration. Functions to load configuration from YAML, validate it against the schema, and save updated configuration back to the file. The default configuration values.

**Why separate**: Configuration loading is a cross-cutting concern that almost every module needs. Centralizing it here with validation ensures that no module ever receives malformed configuration, and it provides a single place to change configuration structure when new options are added.

#### hydra/config/config.py
Defines the `Settings` and `ProviderConfig` Pydantic models. Implements `get_config_path` to locate the active `runtime.yaml` file. Implements `load_settings` to read and validate the configuration, creating a default file if none exists. Implements `save_settings` to persist updated configuration back to disk.

---

### tests/

**Purpose**: Contains all automated tests for the project.

**What belongs here**: Pytest test files organized to mirror the source structure. Unit tests for individual functions and classes. Integration tests for cross-module flows. Test fixtures and mock implementations of provider and memory interfaces.

**Why separate**: Tests must be completely isolated from source code to ensure they do not accidentally share state. The `tests/` directory at the root level is the standard Python convention and is expected by pytest without additional configuration.

---

### .github/workflows/

**Purpose**: Contains GitHub Actions CI workflow definitions.

#### .github/workflows/ci.yml
Defines the CI pipeline that runs on every push and pull request to the main branch. The pipeline sets up Python 3.12, installs uv, syncs all dependencies, runs Black and isort formatting checks, and executes the pytest test suite. A pull request cannot be merged unless this pipeline passes.

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Edge-Explorer/Hydra-Runtime.git
cd Hydra-Runtime

# Create virtual environment using uv
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install all dependencies including dev tools
uv sync --all-extras

# Format code before committing
uv run black hydra tests
uv run isort hydra tests

# Run tests
uv run pytest
```

---

## Roadmap

**Phase 1 - Foundation**: CLI scaffolding, configuration management, SQLite database setup, Rich terminal output, BaseProvider interface, Ollama integration.

**Phase 2 - Memory**: Persistent memory nodes, vector embeddings with FAISS, semantic search, session management, knowledge graph structure.

**Phase 3 - Workspace Intelligence**: Project directory scanning, Project DNA generation, file indexing, git integration.

**Phase 4 - Context Engine**: Context compiler, token budgeting, memory retrieval, prompt assembly.

**Phase 5 - Routing**: Rule-based model router, capability-aware routing, provider switching.

**Phase 6 - Plugins**: Plugin SDK, built-in Git and filesystem plugins, MCP compatibility.

**Phase 7 - Polish**: Comprehensive tests, documentation, benchmarks, CI/CD hardening, PyPI package.

---

## Contributing

This project welcomes contributions. Before opening a pull request, please check the open issues for the task you want to work on or open a new issue describing the change you plan to make. All pull requests must pass the CI pipeline before they can be merged.

---

## License

MIT License. See `LICENSE` for details.