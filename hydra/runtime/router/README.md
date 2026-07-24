# hydra/runtime/router

## Responsibility

This directory contains the model routing logic. The router receives a query and the current session state and decides which provider and model should handle the request.

Routing decisions are based on a combination of query intent classification, configured capability rules, and session state (such as a manually pinned model). The router does not call the provider directly and does not construct the prompt. It returns a routing decision that the command handler uses to select a provider instance.

---

## Rules for This Directory

- The router must not make network calls. It is a pure decision-making module.
- The router must not access the database directly.
- The router must not construct or modify prompts.
- Routing rules must be configurable. Hard-coded model preferences are not acceptable.
- The router must fall back gracefully to the default model if no specific rule matches.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### router.py

**Purpose**: Implements the `ModelRouter` class that selects the appropriate provider and model for a given query.

**What this file must contain**:
- The `ModelRouter` class.
- A `route(query: str, session_state: SessionState) -> RouterDecision` method that classifies the query and returns the selected provider name and model name.
- Intent classification logic (initially keyword-based: detecting terms associated with coding, mathematics, vision, or general reasoning).
- A capability rules table that maps intent categories to preferred providers and models, loaded from configuration.
- A fallback to the session's currently active model if no rule matches or the preferred model is unavailable.
- The `RouterDecision` response is a Pydantic model defined in `hydra/models/schemas.py`.

**What this file must not contain**:
- HTTP calls or provider instantiation.
- Prompt construction.
- Database access.
- Hardcoded model names that cannot be overridden by configuration.

---

## Extending the Router

The routing logic is designed to evolve. Phase 1 uses keyword-based intent classification. Future phases may add:

- Embedding-based semantic intent classification.
- Cost-aware routing that factors in token pricing per provider.
- Latency-aware routing that measures and tracks provider response times.
- ML-based routing that learns from past query-model performance pairs.

All such extensions should be implemented as additional methods or strategy classes within this directory without changing the `route()` interface.
