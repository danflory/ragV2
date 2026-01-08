# Task 2.3: Ollama Local Models Wrapper

**File**: `app/wrappers/ollama_wrapper.py`

## Requirements
- [x] Inherit from `GravitasAgentWrapper`
- [x] Implement `__init__(session_id: str, model_name: str, ollama_url: str = "http://localhost:11434")`
    - [x] Call super with `f"Ollama_{model_name}"`, target model, and "L1"
- [x] Implement `async def _execute_internal(task: dict) -> dict`
    - [x] Use `httpx.AsyncClient` to stream from Ollama API
    - [x] Handle JSON stream lines
    - [x] Parse thoughts and actions
    - [x] Log metrics (total_tokens)
- [x] Implement `def _parse_thought(chunk: dict) -> Optional[str]`
    - [x] Parse custom `<think>` tags via regex
- [x] Implement `def _parse_action(chunk: dict) -> Optional[str]`
    - [x] Parse custom `<action>` tags via regex

## Environment Setup
- [x] Ensure Ollama is running on localhost:11434
- [x] Pull models for testing: `codellama:7b`, `qwen2.5:7b`, `llama3:8b`

## Test Task
- [x] Verify with prompt: "Write a Python function to calculate factorial"
- [x] Expected: ReasoningPipe file with THOUGHT/ACTION entries if tags are used
