# hydra/utils

## Responsibility

This directory contains shared utility functions that are used by multiple modules but do not belong to any specific module. Utilities are stateless helper functions with no side effects beyond what is explicitly described.

---

## Rules for This Directory

- Utilities must be stateless. They must not maintain any internal state between calls.
- Utilities must not make database calls, network calls, or filesystem writes.
- If a function is only used by one module, it belongs in that module, not here.
- No business logic belongs here. Utilities are infrastructure helpers, not domain logic.
- Every utility function must have a complete docstring and type annotations.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### helpers.py

**Purpose**: Contains general-purpose utility functions used across the runtime.

**What this file must contain**:

- `estimate_tokens(text: str) -> int`: Estimates the number of tokens in a string using a character-based heuristic (approximately 4 characters per token). This avoids a hard dependency on tiktoken for providers that do not use GPT tokenization.
- `truncate_to_token_limit(text: str, max_tokens: int) -> str`: Truncates a string to approximately the specified token count while preserving whole words.
- `read_file_safe(path: str) -> str | None`: Reads a file from the filesystem with encoding detection. Returns `None` if the file cannot be read rather than raising an exception.
- `normalize_path(path: str) -> str`: Normalizes a file path to use forward slashes and resolves `..` components, ensuring consistent path representation across operating systems.
- `format_timestamp(dt: datetime) -> str`: Formats a datetime object as a human-readable string in the project's standard format.
- `truncate_middle(text: str, max_length: int) -> str`: Truncates long strings in the middle with an ellipsis, preserving the start and end. Useful for displaying file paths in terminal output.
