# hydra/runtime/providers

## Responsibility

This directory abstracts all communication with AI model providers behind a single, consistent interface. Every supported provider (Ollama, Gemini, OpenAI, Groq, Anthropic, etc.) is implemented as a separate file that inherits from the `BaseProvider` abstract class.

The rest of the runtime interacts only with `BaseProvider`. It never references a concrete provider class directly. This ensures that swapping providers or adding new ones requires no changes to the compiler, router, or any other module.

---

## Rules for This Directory

- All HTTP calls to external services must originate from this directory only. No other module is permitted to make HTTP requests to AI providers.
- Every provider must implement all abstract methods defined in `base.py`.
- Provider files must not contain routing logic, prompt construction logic, or memory access.
- Provider files should handle only the communication protocol for their respective service: request formatting, HTTP transport, response parsing, and error handling.
- Sensitive credentials such as API keys must be read from the configuration, never hardcoded.

---

## Files

### \_\_init\_\_.py

Marks this directory as a Python package. May export a `PROVIDER_REGISTRY` dictionary that maps provider name strings to their classes for use by the router and CLI.

### base.py

**Purpose**: Defines the abstract interface that every model provider must implement.

**What this file must contain**:
- The `BaseProvider` abstract class inheriting from `abc.ABC`.
- The `generate(prompt, system_prompt, **kwargs) -> str` abstract method for full response generation.
- The `generate_stream(prompt, system_prompt, **kwargs) -> Generator[str, None, None]` abstract method for streaming response generation.
- The `list_models() -> list[str]` abstract method for listing available models from the provider.
- The `health_check() -> bool` abstract method for verifying provider availability.
- Pydantic models for the standard request and response structures, imported from `hydra/models/schemas.py`.

**What this file must not contain**:
- Any network calls.
- Any provider-specific logic.
- Any routing or compilation logic.

### ollama.py

**Purpose**: Implements `BaseProvider` for the Ollama local inference server.

**What this file must contain**:
- The `OllamaProvider` class inheriting from `BaseProvider`.
- HTTP communication with the Ollama REST API using `httpx`.
- Implementation of `generate` using the `/api/generate` endpoint.
- Implementation of `generate_stream` using the streaming variant of the same endpoint.
- Implementation of `list_models` using the `/api/tags` endpoint.
- Implementation of `health_check` by pinging the Ollama base URL.
- Ollama-specific error handling and response parsing.

**What this file must not contain**:
- Logic from any other provider.
- Prompt construction or memory access.

---

## Adding a New Provider

To add a new provider:

1. Create a new file in this directory named after the provider (e.g., `gemini.py`).
2. Create a class that inherits from `BaseProvider`.
3. Implement all abstract methods.
4. Register the provider in `__init__.py` by adding it to the `PROVIDER_REGISTRY`.
5. Add any required API keys or configuration fields to the `ProviderConfig` model in `hydra/models/schemas.py`.
6. Write unit tests in `tests/runtime/providers/test_<provider_name>.py` using mocked HTTP responses.
