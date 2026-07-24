# hydra/models

## Responsibility

This directory contains all Pydantic data schemas used across the project. These schemas define the data contracts between modules: the structures that modules produce and consume when communicating with each other.

These are not database models. Database ORM models are defined in `hydra/database/models.py`. The Pydantic schemas here are the runtime data structures, validated and typed, that flow between the CLI, the runtime, and the database layer.

---

## Rules for This Directory

- Every data structure that crosses a module boundary must be defined as a Pydantic model here.
- Schemas must be pure data definitions. No business logic, database calls, or HTTP calls belong in schemas.
- Schemas should be immutable where possible. Use `model_config = ConfigDict(frozen=True)` for schemas that represent completed data records.
- When a schema changes, all modules that use it must be updated. Backward compatibility should be maintained where possible.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### schemas.py

**Purpose**: Defines all Pydantic BaseModel classes used as data contracts between runtime modules.

**What this file must contain**:

- `ProviderRequest`: The input structure for a model generation request, containing `prompt`, `system_prompt`, `model`, `max_tokens`, and `temperature`.
- `ProviderResponse`: The output structure from a provider, containing `content`, `model`, `provider`, `token_count`, and `latency_ms`.
- `MemoryNode`: The runtime representation of a memory node, containing `id`, `node_type`, `content`, `metadata`, `session_id`, `created_at`, and `relevance_score` (populated on retrieval).
- `MemoryEdge`: The runtime representation of a graph edge, containing `source_id`, `target_id`, and `relationship`.
- `ProjectDNA`: The analyzed project metadata, containing `language`, `framework`, `package_manager`, `entry_points`, `database_type`, `architecture_hints`, and `scanned_at`.
- `SessionState`: The live runtime state, containing `session_id`, `goal`, `active_model`, `active_provider`, `current_branch`, `tasks`, `constraints`, `recent_files`, and `updated_at`.
- `Session`: The session record, containing `id`, `workspace_path`, `name`, `is_active`, and `created_at`.
- `Checkpoint`: The checkpoint record, containing `id`, `session_id`, `name`, `state_snapshot`, and `created_at`.
- `RouterDecision`: The routing output, containing `provider`, `model`, `intent`, and `reason`.
- `ContextPayload`: The compiler output, containing `system_prompt`, `user_message`, `token_estimate`, `memory_nodes_used`, and `model_hint`.
- `PluginResult`: The plugin execution result, containing `success`, `output`, and `error`.
