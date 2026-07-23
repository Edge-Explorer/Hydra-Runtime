# Hydra Runtime 🐉

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Modular](https://img.shields.io/badge/architecture-modular-orange.svg)](#high-level-architecture)

> **An AI Runtime that manages memory, context, routing, state, and workspaces independently of any LLM.**

Hydra Runtime is not just another CLI to chat with LLMs. It is a decoupling layer (runtime environment) between AI agents/models and the developer's workspace. By treating LLMs as swappable plugins, Hydra maintains persistent memory, local project DNA, session routing, and dynamic context assembly, ensuring that AI models never lose context during workspace switches or model handoffs.

---

## 👁️ The Vision

Every AI engineer faces the same productivity bottleneck: **context loss**. You have multiple models (one optimized for coding, one for speed, one for reasoning), multiple active conversations, and a complex workspace. When you switch models or start a new thread, the context is shattered.

Hydra solves this by acting as an **Operating System for AI interaction**:
*   **Decoupled Orchestration**: The LLM is a pluggable backend. The runtime handles the memory, state, and tools.
*   **Project DNA Workspace Scanning**: Hydra understands the programming language, framework, design patterns, and constraints of your project.
*   **Memory Graph**: Conversations are stored as semantically linked nodes (Decisions, Tasks, Bugs, Classes, APIs) rather than a linear message list.
*   **Context Compiler**: Compresses and builds optimized prompts based on live git diffs, current workspace state, and memory query responses.

---

## 📐 High-Level Architecture

```
                       ┌──────────────────────┐
                       │  Typer Command CLI   │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │  Command Dispatcher  │
                       └──────────┬───────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Model Router   │      │    Workspace    │      │  Memory Graph   │
│ (Rule/Capability│      │   Intelligence  │      │  & Vector DB    │
└─────────┬───────┘      └────────┬────────┘      └────────┬────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Model Providers │      │   Project DNA   │      │ Knowledge Graph │
│ (Ollama/Gemini) │      │  (Config/AST)   │      │   SQLite DB     │
└─────────┬───────┘      └────────┬────────┘      └────────┬────────┘
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ▼
                       ┌──────────────────────┐
                       │   Context Compiler   │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    Selected Model    │
                       └──────────────────────┘
```

---

## 🛠️ Tech Stack & Key Choices

*   **Language**: Python 3.12+ (leveraging the rich AI ecosystem, modern type hints, and CLI frameworks).
*   **CLI Framework**: [Typer](https://typer.tiangolo.com/) (for robust command generation, autocomplete, and clean subcommands).
*   **Terminal UI**: [Rich](https://rich.readthedocs.io/) (for progress bars, trees, markdown rendering, syntax highlighting, and live dashboard panels).
*   **Persistence**: SQLite with [SQLAlchemy 2.0 ORM](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/) for schema migrations.
*   **Vector Search**: FAISS (local, fast CPU-based index) combined with `sentence-transformers` (`BAAI/bge-small-en-v1.5`) for local semantic retrieval.
*   **Memory / Relationships**: SQLite for structured relationships (Graph-like structure via tables) and `networkx` for runtime graph analysis.

---

## 📂 Project Directory Structure

```
hydra/
│
├── cli/                 # Typer application instantiation & shell completion
├── commands/            # CLI Command handlers (ask, switch, memory, status, etc.)
├── runtime/             # Core Runtime Logic
│   ├── router/          # Dynamic model routing (capability & cost-aware)
│   ├── compiler/        # Context compiler, token budgeting, prompt assembly
│   ├── workspace/       # Project DNA extraction, framework detection
│   ├── memory/          # Vector embeddings store & memory retrieval
│   ├── providers/       # Model provider clients (Ollama, Gemini, OpenAI, Groq)
│   ├── graph/           # Knowledge graph, entities (Decisions, Bugs, APIs)
│   ├── plugins/         # Extensible interfaces for Git, Docker, Terminal, MCP
│   ├── checkpoints/     # Session state rollback and branch restorations
│   ├── state/           # Runtime active state manager (goals, open tasks)
│   └── session/         # Workspace projects session manager
│
├── database/            # SQLite schemas, connection session makers, migrations
├── models/              # Pydantic core data schemas and settings
├── utils/               # Logging, formatting, token count helpers
├── config/              # YAML parsing, Pydantic-Settings integrations
├── tests/               # Pytest suite
├── docs/                # Developer guides and API specifications
└── examples/            # Example project setups and client scenarios
```

---

## 🗺️ Implementation Roadmap

### Phase 1: Foundation
*   [ ] CLI scaffolding with Typer commands (`hydra init`, `hydra ask`, `hydra status`, `hydra config`).
*   [ ] Configuration management using YAML and `pydantic-settings`.
*   [ ] Database schema setup with SQLite & SQLAlchemy ORM.
*   [ ] Command execution feedback using Rich panels, spinners, and tables.
*   [ ] Swappable model provider interface (`BaseProvider`) and Ollama client integration.

### Phase 2: Memory & Context
*   [ ] SQLite memory schemas and vector search module using FAISS.
*   [ ] Local embeddings generation using sentence-transformers.
*   [ ] Session-specific memory tracking and knowledge graph associations.
*   [ ] Git-informed workspace scanning for contextual prompt compiler inputs.