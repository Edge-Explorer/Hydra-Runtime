# hydra/runtime/state

## Responsibility

This directory manages the live runtime state for the currently active session. The state is the runtime's understanding of what is happening right now: what the developer is working on, what model is active, what branch is checked out, what tasks are open, and what constraints apply.

The state persists between terminal sessions using the SQLite database, so the developer can close and reopen their terminal without losing context.

---

## Rules for This Directory

- The state manager is the single source of truth for the current session's live data.
- All other modules that need current state must read it through the `StateManager`. They must not query the database for session state directly.
- State writes must be immediately persisted to the database to prevent data loss on unexpected process termination.
- The state manager must not make network calls or perform filesystem scanning.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### state.py

**Purpose**: Implements the `StateManager` class that tracks and persists the live session state.

**What this file must contain**:

- The `StateManager` class initialized with the workspace ID and database session.
- A `load() -> SessionState` method that reads the current state from the database on startup.
- A `get() -> SessionState` method that returns the in-memory cached state.
- Individual setter methods for each state field:
  - `set_goal(goal: str) -> None`
  - `set_active_model(provider: str, model: str) -> None`
  - `set_current_branch(branch: str) -> None`
  - `add_task(task: str) -> None`
  - `complete_task(task_id: str) -> None`
  - `add_constraint(constraint: str) -> None`
  - `add_recent_file(file_path: str) -> None`
- Each setter must update the in-memory state and immediately persist the change to the database.
- A `reset() -> None` method that resets the state to defaults for the current workspace.
- A `snapshot() -> SessionState` method that returns a copy of the current state for checkpointing.

**What this file must not contain**:
- Checkpoint creation logic (that belongs in `hydra/runtime/checkpoints/manager.py`).
- Memory or graph operations.
- HTTP calls.
- Terminal output.
