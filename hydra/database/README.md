# hydra/database

## Responsibility

This directory contains all database infrastructure. It defines the SQLAlchemy engine, the session factory, the declarative ORM base class, and all ORM table models. It is the lowest layer of the persistence stack and knows nothing about business logic.

---

## Rules for This Directory

- No business logic, routing logic, compilation logic, or runtime decisions belong here.
- This directory defines the database structure. It does not enforce domain rules.
- All ORM models must inherit from the `Base` class defined in `db.py`.
- No module outside this directory should create database engine instances or direct connections. All database access must go through the `SessionLocal` factory or the `get_db` context manager.
- Schema changes must be managed through Alembic migrations. Direct schema alterations in production are not permitted.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### db.py

**Purpose**: Creates the database engine and provides the session factory used across the application.

**What this file must contain**:

- Creation of the SQLAlchemy `engine` using the database URL loaded from the configuration.
- Definition of the `SessionLocal` session factory using `sessionmaker`.
- Definition of the `Base` declarative class that all ORM models inherit from.
- A `get_db()` context manager function that yields a database session and ensures it is closed after use.
- An `init_db()` function that creates all tables by calling `Base.metadata.create_all(engine)`. This is called once during `hydra init`.

**What this file must not contain**:
- ORM model definitions (those belong in `models.py`).
- Business logic.
- Migration logic (that is handled by Alembic).

### models.py

**Purpose**: Defines all SQLAlchemy ORM table models that map to database tables.

**What this file must contain**:

- The `Session` ORM model with columns: `id`, `workspace_path`, `name`, `is_active`, `created_at`, `updated_at`.
- The `SessionState` ORM model with columns: `id`, `session_id` (foreign key to `Session`), `goal`, `active_model`, `active_provider`, `current_branch`, `tasks` (JSON), `constraints` (JSON), `recent_files` (JSON), `updated_at`.
- The `MemoryNode` ORM model with columns: `id`, `session_id`, `node_type`, `content`, `metadata` (JSON), `embedding_index` (integer index in the FAISS array), `created_at`.
- The `MemoryEdge` ORM model with columns: `id`, `source_id` (foreign key to `MemoryNode`), `target_id` (foreign key to `MemoryNode`), `relationship`, `created_at`.
- The `Checkpoint` ORM model with columns: `id`, `session_id`, `name`, `state_snapshot` (JSON), `created_at`.
- The `ProjectDNA` ORM model with columns: `id`, `session_id`, `language`, `framework`, `package_manager`, `entry_points` (JSON), `database_type`, `architecture_hints` (JSON), `scanned_at`.

**What this file must not contain**:
- The engine or session factory (those belong in `db.py`).
- Business logic.
- Pydantic models (those belong in `hydra/models/schemas.py`).
