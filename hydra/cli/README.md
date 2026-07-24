# hydra/cli

## Responsibility

This directory is the entry point of the entire Hydra Runtime command line interface. It contains the Typer application instance and the wiring that connects all command groups to the CLI.

This directory does not contain any business logic. Its sole purpose is to initialize the CLI application and register all commands from the `hydra/commands/` directory.

---

## Rules for This Directory

- Do not place business logic here. All logic belongs in `hydra/commands/` or the runtime modules.
- Do not import database models or runtime internals directly into this directory.
- Do not define command handlers here. Commands are defined in `hydra/commands/`.
- This directory should remain minimal and rarely need changes.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package. Should remain empty or contain only a brief module-level docstring.

### main.py

**Purpose**: Creates the root Typer application instance and registers all command groups.

**What this file must contain**:
- Import of `typer` and creation of the `app = typer.Typer(...)` instance with the application name, help text, and version information.
- Import and registration of all command modules from `hydra/commands/` using `app.add_typer()`.
- The `if __name__ == "__main__"` block that allows running the CLI directly during development.
- Rich exception handling configuration if applicable.

**What this file must not contain**:
- Any command handler logic.
- Any imports from `hydra/runtime/`, `hydra/database/`, or `hydra/config/` beyond what is needed to initialize the app.
- Any business logic of any kind.

**Example structure**:
```python
import typer
from hydra.commands import ask, init, status, switch, memory, config

app = typer.Typer(
    name="hydra",
    help="Hydra Runtime: AI orchestration runtime layer.",
    no_args_is_help=True,
)

app.add_typer(ask.app, name="ask")
app.add_typer(init.app, name="init")
# ... and so on

if __name__ == "__main__":
    app()
```
