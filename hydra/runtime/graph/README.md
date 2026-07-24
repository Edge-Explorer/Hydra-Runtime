# hydra/runtime/graph

## Responsibility

This directory manages the knowledge graph that represents structural relationships between memory nodes. While the memory store handles semantic similarity (finding nodes with similar meaning), the knowledge graph handles structural relationships (finding nodes that are directly connected by a defined relationship type).

Together, the memory store and the knowledge graph provide two complementary retrieval strategies. The compiler uses both to build the richest possible context for a query.

---

## Rules for This Directory

- The knowledge graph must be built on top of the memory nodes managed by `hydra/runtime/memory/`. It does not maintain its own separate node storage.
- The in-memory networkx graph is the working representation. The edges (relationships) are persisted to the SQLite database via the `MemoryEdge` ORM model.
- This directory must not construct prompts, make HTTP calls, or perform filesystem scanning.
- Graph traversal depth must be configurable and bounded to prevent runaway queries.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### graph.py

**Purpose**: Implements the `KnowledgeGraph` class that manages typed edges between memory nodes and provides traversal methods.

**What this file must contain**:

- The `KnowledgeGraph` class initialized with the workspace ID.
- An `add_edge(source_id: str, target_id: str, relationship: str) -> None` method that:
  1. Adds a directed edge to the in-memory networkx graph.
  2. Persists the edge to the `memory_edges` table in SQLite.
- A `remove_edge(source_id: str, target_id: str) -> None` method.
- A `get_related(node_id: str, depth: int) -> list[str]` method that traverses the graph from a starting node up to the specified depth and returns a list of related node IDs.
- A `get_neighbors(node_id: str, relationship: str) -> list[str]` method that returns immediate neighbors connected by a specific relationship type.
- A `load_from_db() -> None` method that reconstructs the in-memory graph from persisted edges in SQLite on startup.
- A `to_dict() -> dict` method that serializes the graph to a dictionary for terminal rendering.

**What this file must not contain**:
- Memory node content or embedding logic (that belongs in `hydra/runtime/memory/store.py`).
- Prompt construction.
- HTTP calls.

---

## Edge Relationship Types

| Relationship   | Meaning                                                   |
|----------------|-----------------------------------------------------------|
| `depends_on`   | Source node requires target node to function              |
| `implements`   | Source node is an implementation of target node           |
| `references`   | Source node mentions or uses target node                  |
| `fixes`        | Source node resolves the bug described by target node     |
| `modifies`     | Source node changes the file or entity of target node     |
| `relates_to`   | Generic relationship for loosely connected nodes          |
