# hydra/runtime/plugins

## Responsibility

This directory defines the plugin system that allows external tools and services to be integrated into the Hydra Runtime without modifying the core modules. Plugins extend what the runtime can do by providing additional context, executing actions, or bridging to external APIs and services.

Built-in plugins for Git, the filesystem, and the terminal are implemented here. Third-party plugins can be distributed as separate Python packages that implement the same `BasePlugin` interface and are auto-discovered at startup.

---

## Rules for This Directory

- All plugins must inherit from `BasePlugin` defined in `base.py`.
- Plugins must not import from each other. Each plugin is independent.
- Plugins must handle their own errors. A failing plugin must not crash the runtime.
- Plugins must declare their capabilities and requirements explicitly so the runtime can determine whether a plugin is available in the current environment.
- Built-in plugins are located directly in this directory. Third-party plugins are discovered via Python entry points.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package. Contains the plugin loader that discovers and registers all available plugins.

### base.py

**Purpose**: Defines the abstract `BasePlugin` interface that all plugins must implement.

**What this file must contain**:

- The `BasePlugin` abstract class inheriting from `abc.ABC`.
- A `name` abstract property that returns the plugin's unique identifier string.
- A `description` abstract property that returns a human-readable description.
- An `is_available() -> bool` abstract method that checks whether the plugin's external dependencies are met (e.g., Git is installed, Docker daemon is running).
- An `initialize(config: dict) -> None` abstract method called once when the plugin is loaded.
- An `execute(action: str, params: dict) -> PluginResult` abstract method that runs a specific plugin action.
- The `PluginResult` Pydantic model containing `success`, `output`, and `error` fields, defined in `hydra/models/schemas.py`.

**What this file must not contain**:
- Any plugin-specific implementation logic.
- Network calls.
- Database access.

---

## Adding a Plugin

To add a built-in plugin:

1. Create a new file in this directory named after the tool (e.g., `docker.py`).
2. Create a class that inherits from `BasePlugin`.
3. Implement all abstract methods.
4. Register the plugin class in `__init__.py`.
5. Write tests in `tests/runtime/plugins/test_<plugin_name>.py`.

To add a third-party plugin (for external contributors):

1. Create a Python package that defines a class inheriting from `BasePlugin`.
2. Declare the class as a `hydra.plugins` entry point in the package's `pyproject.toml`.
3. When Hydra starts, the plugin loader scans for installed entry points and registers them automatically.
