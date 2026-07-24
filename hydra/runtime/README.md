# hydra/runtime

## Responsibility

This directory is the core of Hydra Runtime. It contains all the intelligence of the system: model routing, context compilation, workspace analysis, memory management, knowledge graph construction, plugin orchestration, session state, checkpointing, and session lifecycle management.

Nothing in this directory should import from `hydra/cli/` or `hydra/commands/`. The runtime is designed to be completely decoupled from the CLI so that it can be used in a future web interface, API server, or Python SDK without modification.

---

## Rules for This Directory

- No module in this directory should import from `hydra/cli/` or `hydra/commands/`.
- No module should render terminal output directly. Output formatting belongs in the command handlers.
- Every swappable capability (providers, memory store, plugins) must be defined behind an abstract base class.
- Runtime modules should communicate through the shared Pydantic schemas defined in `hydra/models/schemas.py`.
- Database access must go through the session factory in `hydra/database/db.py`.

---

## Subdirectories

### providers/

Contains the abstract `BaseProvider` interface and all concrete model provider implementations. Every supported AI service (Ollama, Gemini, OpenAI, Groq, etc.) has its own file here. The rest of the runtime interacts only with the `BaseProvider` interface, never with a concrete implementation directly.

See `hydra/runtime/providers/README.md` for full details.

### router/

Contains the `ModelRouter` that decides which provider and model to use for a given query. The router evaluates query intent and session state to select the most appropriate model based on configured capability rules.

See `hydra/runtime/router/README.md` for full details.

### compiler/

Contains the `ContextCompiler` that builds the complete prompt payload sent to the model. The compiler gathers workspace DNA, memory nodes, git diff, session state, and user query, then assembles and compresses them into a structured prompt within the token budget.

See `hydra/runtime/compiler/README.md` for full details.

### workspace/

Contains the `WorkspaceAnalyzer` that scans a project directory to build the Project DNA. The DNA describes the detected language, framework, dependencies, entry points, database setup, and architecture style.

See `hydra/runtime/workspace/README.md` for full details.

### memory/

Contains the `MemoryStore` that manages persistent, semantically searchable memory. Memory is stored as typed nodes in SQLite with vector embeddings indexed by FAISS for similarity search.

See `hydra/runtime/memory/README.md` for full details.

### graph/

Contains the `KnowledgeGraph` that manages structural relationships between memory nodes using typed edges. The graph layer complements the vector memory layer by enabling relationship-based context retrieval.

See `hydra/runtime/graph/README.md` for full details.

### plugins/

Contains the abstract `BasePlugin` interface and built-in plugin implementations. Plugins extend the runtime's capabilities by integrating external tools such as Git, the filesystem, Docker, and third-party services.

See `hydra/runtime/plugins/README.md` for full details.

### checkpoints/

Contains the `CheckpointManager` that handles snapshotting and restoring session state. Checkpoints are named records of the complete session state at a specific point in time.

See `hydra/runtime/checkpoints/README.md` for full details.

### state/

Contains the `StateManager` that tracks the live runtime state for the current session. The state includes the active goal, open tasks, active model, current git branch, recent files, and constraints.

See `hydra/runtime/state/README.md` for full details.

### session/

Contains the `SessionManager` that manages the lifecycle of workspace sessions. Each workspace has an independent session with its own state, memory, and checkpoints.

See `hydra/runtime/session/README.md` for full details.
