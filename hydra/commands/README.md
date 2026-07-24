# hydra/commands

## Responsibility

This directory contains one file per CLI command group. Each file defines the command handler functions that are invoked when a user runs a specific `hydra` command.

Command handlers in this directory are intentionally thin. They accept user input from the CLI, pass it to the appropriate runtime module, and render the result to the terminal using Rich. All business logic lives in `hydra/runtime/`.

---

## Rules for This Directory

- Command handlers must not contain business logic. They must delegate all processing to runtime modules.
- Command handlers must not make direct database calls or HTTP requests.
- All terminal output must use Rich. Do not use bare `print()` statements.
- Each file corresponds to one logical command group. Do not combine unrelated commands in a single file.
- Input validation that is specific to the CLI (such as checking that a required argument is provided) is acceptable here. Data validation belongs in the runtime or in Pydantic models.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package. Should remain empty.

### init.py

**Command**: `hydra init`

**Purpose**: Initializes a new Hydra workspace in the current directory.

**What this handler does**:
- Calls the `WorkspaceAnalyzer` to scan the current directory and build the Project DNA.
- Calls the database initialization function to create the SQLite database and run migrations.
- Calls the configuration module to generate a default `runtime.yaml` if one does not exist.
- Creates an initial session for the workspace.
- Renders a Rich panel summarizing what was detected and what was created.

### ask.py

**Command**: `hydra ask "<query>"`

**Purpose**: Sends a query to the currently active model with full compiled context.

**What this handler does**:
- Accepts the user's query string as a required argument.
- Calls the `ContextCompiler` to build the full prompt payload.
- Calls the `ModelRouter` to determine the appropriate provider and model.
- Calls the selected provider's `generate` or `generate_stream` method.
- Streams or renders the model response using Rich Markdown.

### switch.py

**Command**: `hydra switch`

**Purpose**: Switches the active model or provider.

**What this handler does**:
- Lists available configured providers and models in a Rich table.
- Accepts a provider name and model name as arguments.
- Calls the `StateManager` to update the active model.
- Confirms the switch with a Rich success message.

### memory.py

**Command**: `hydra memory`

**Purpose**: Provides subcommands for inspecting and managing the memory store.

**Subcommands**:
- `hydra memory list`: Lists all memory nodes with their types and timestamps.
- `hydra memory search "<query>"`: Performs a semantic search against the memory store.
- `hydra memory delete <id>`: Deletes a specific memory node by ID.
- `hydra memory clear`: Clears all memory nodes for the current workspace (with confirmation prompt).

### status.py

**Command**: `hydra status`

**Purpose**: Displays the current runtime and session state.

**What this handler does**:
- Reads the current session from the `SessionManager`.
- Reads the current state from the `StateManager`.
- Renders a Rich panel or table showing: active model, active provider, current workspace, current git branch, active goal, open tasks, memory node count, and last activity timestamp.

### config.py

**Command**: `hydra config`

**Purpose**: Provides subcommands for reading and updating configuration values.

**Subcommands**:
- `hydra config show`: Displays the full current configuration as a Rich table.
- `hydra config set <key> <value>`: Updates a specific configuration key.
- `hydra config reset`: Resets the configuration to default values after confirmation.
