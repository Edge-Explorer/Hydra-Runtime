# hydra/runtime/compiler

## Responsibility

This directory contains the context compiler, which is the most critical component of the runtime. The compiler is responsible for assembling everything the model needs to know before responding to a query.

A raw user query is never sent directly to a model in Hydra. Instead, the compiler retrieves relevant context from multiple sources, applies a token budget to stay within the model's context window, and assembles a structured prompt payload that the provider sends to the model.

---

## Rules for This Directory

- The compiler is the only module permitted to construct or assemble prompts.
- The compiler must apply token budget limits. It must never assemble a prompt that exceeds the configured maximum token count.
- The compiler must not make provider API calls. It produces a payload that the provider sends.
- The compiler must retrieve memory context through the `MemoryStore` interface, not by querying the database directly.
- The compiler must retrieve workspace context through the `WorkspaceAnalyzer` output, not by scanning the filesystem directly.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### compiler.py

**Purpose**: Implements the `ContextCompiler` class that builds the complete prompt payload for a model request.

**What this file must contain**:

- The `ContextCompiler` class.
- A `compile(query: str, session_state: SessionState) -> ContextPayload` method that performs the full compilation pipeline.
- The compilation pipeline includes the following steps in order:
  1. Retrieve the Project DNA from the active workspace.
  2. Retrieve the current git branch and diff from the Git plugin or GitPython.
  3. Query the `MemoryStore` with the user's query to retrieve semantically similar memory nodes.
  4. Query the `KnowledgeGraph` for structurally related nodes if applicable.
  5. Read the current goal and active tasks from the `StateManager`.
  6. Assemble a system prompt incorporating workspace DNA, constraints, and coding style.
  7. Assemble the user message incorporating memory context, recent files, git diff, and the user's query.
  8. Estimate the total token count using the utilities in `hydra/utils/helpers.py`.
  9. If the token count exceeds the budget, apply compression: truncate memory context first, then git diff, then file contents, preserving the user query and system prompt always.
  10. Return a `ContextPayload` Pydantic model containing the system prompt, user message, and metadata.

**What this file must not contain**:
- Provider API calls.
- Database queries.
- Filesystem scanning.
- Command handler logic or terminal output.

---

## Context Payload Structure

The `ContextPayload` returned by the compiler is defined in `hydra/models/schemas.py`. It contains:

- `system_prompt`: The assembled system context including workspace DNA and constraints.
- `user_message`: The assembled user message including memory, diff, and the query.
- `token_estimate`: The estimated total token count of the payload.
- `memory_nodes_used`: The list of memory node IDs included in the context.
- `model_hint`: Optional suggestion to the router about which model capability is needed.
