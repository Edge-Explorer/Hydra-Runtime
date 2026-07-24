# hydra/runtime/session

## Responsibility

This directory manages the lifecycle of workspace sessions. A session associates a workspace directory with its own independent state, memory store, knowledge graph, and checkpoints. Hydra supports multiple workspace sessions simultaneously, each completely isolated from the others.

---

## Rules for This Directory

- Each workspace directory maps to exactly one session at a time. There cannot be two active sessions for the same workspace directory simultaneously.
- The session manager must not manage state data directly. State management is delegated to `hydra/runtime/state/state.py`.
- The session manager must not access the memory store or graph directly. Those are initialized by their own modules once the session is activated.
- Deleting a session must cascade to delete all associated state, memory nodes, graph edges, and checkpoints.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### session.py

**Purpose**: Implements the `SessionManager` class that handles session creation, activation, listing, and deletion.

**What this file must contain**:

- The `SessionManager` class initialized with the database session.
- A `create(workspace_path: str, name: str) -> Session` method that:
  1. Validates that no session exists for the given workspace path.
  2. Creates a `Session` record in the database.
  3. Initializes a default `SessionState` for the new session.
  4. Returns the created `Session` Pydantic model.
- A `activate(session_id: str) -> Session` method that marks a session as the active one for its workspace.
- A `get_active(workspace_path: str) -> Session` method that returns the currently active session for a workspace.
- A `list_all() -> list[Session]` method that returns all sessions across all workspaces.
- A `list_for_workspace(workspace_path: str) -> list[Session]` method.
- A `delete(session_id: str) -> None` method that removes the session and cascades deletion to all associated data.
- A `get_or_create(workspace_path: str) -> Session` convenience method used by `hydra init` to ensure a session always exists.

**What this file must not contain**:
- State field management (that belongs in `hydra/runtime/state/state.py`).
- Memory or graph operations.
- HTTP calls.
- Filesystem scanning.
