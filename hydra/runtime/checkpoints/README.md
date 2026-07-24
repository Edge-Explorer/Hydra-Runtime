# hydra/runtime/checkpoints

## Responsibility

This directory manages session state checkpoints. A checkpoint is a named, timestamped snapshot of the complete session state at a specific point in time. Checkpoints allow the developer to save a known-good state and restore it later if the session drifts in an undesirable direction.

This is conceptually similar to git commits but for AI session context rather than source code.

---

## Rules for This Directory

- Checkpoints must capture the complete session state as defined by the `SessionState` Pydantic model.
- Checkpoint records are persisted to the SQLite database. The checkpoint manager must not write to any other storage location.
- Restoring a checkpoint must replace the current session state entirely. Partial restoration is not supported in the initial implementation.
- Checkpoints must not be modified after creation. They are immutable records.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### manager.py

**Purpose**: Implements the `CheckpointManager` class that handles creating, listing, restoring, and deleting checkpoints.

**What this file must contain**:

- The `CheckpointManager` class initialized with the workspace ID and database session.
- A `create(name: str, session_state: SessionState) -> Checkpoint` method that:
  1. Serializes the current session state to JSON.
  2. Saves a `Checkpoint` record to the database with the provided name, timestamp, and serialized state.
  3. Returns the created `Checkpoint` Pydantic model.
- A `list(workspace_id: str) -> list[Checkpoint]` method that returns all checkpoints for a workspace ordered by creation time.
- A `restore(checkpoint_id: str) -> SessionState` method that:
  1. Retrieves the checkpoint record from the database.
  2. Deserializes the state JSON back into a `SessionState` Pydantic model.
  3. Returns the restored state for the `StateManager` to apply.
- A `delete(checkpoint_id: str) -> None` method.
- A `prune(workspace_id: str, keep_last: int) -> None` method that deletes all but the most recent `keep_last` checkpoints.

**What this file must not contain**:
- State management logic (that belongs in `hydra/runtime/state/state.py`).
- Memory or graph operations.
- HTTP calls.
