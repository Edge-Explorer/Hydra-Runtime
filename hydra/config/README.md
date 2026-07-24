# hydra/config

## Responsibility

This directory manages loading, validating, and persisting the Hydra Runtime configuration. Configuration is stored in a `runtime.yaml` file located either in the current workspace directory or in the user's home directory under `~/.hydra/`.

This is a cross-cutting concern that almost every other module depends on. Centralizing it here with Pydantic validation ensures that no module ever receives malformed or missing configuration values.

---

## Rules for This Directory

- All configuration access throughout the project must go through the `load_settings()` function defined here. Modules must not read environment variables or YAML files directly.
- Configuration must always be validated against the Pydantic `Settings` model before use. Invalid configuration must produce a clear error message, not a runtime crash.
- If no configuration file exists, a valid default configuration must be generated automatically.
- Sensitive values such as API keys must be treated carefully: they must not be logged and must be marked as secret in the Pydantic model where applicable.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package.

### config.py

**Purpose**: Defines the configuration schema and provides the load and save functions used across the runtime.

**What this file must contain**:

- The `ProviderConfig` Pydantic model with fields: `name`, `base_url`, `api_key`, `default_model`.
- The `Settings` Pydantic model with fields: `default_provider`, `default_model`, `db_url`, `workspace_dir`, and `providers` (a dictionary of `ProviderConfig` instances keyed by provider name).
- A `get_config_path() -> Path` function that searches for `runtime.yaml` in the current directory first, then in `~/.hydra/`.
- A `save_settings(settings: Settings, path: Path | None) -> None` function that serializes the settings to YAML and writes them to the config path.
- A `load_settings() -> Settings` function that reads and validates `runtime.yaml`, creating a default configuration file if none is found.

**What this file must not contain**:
- Business logic.
- Database access.
- HTTP calls.
- Any runtime module imports.
