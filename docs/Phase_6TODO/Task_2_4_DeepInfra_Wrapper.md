# Task 2.4: DeepInfra (Qwen2.5-Coder) Wrapper

**File**: `app/wrappers/deepinfra_wrapper.py`

## Requirements
- [x] Inherit from `GravitasAgentWrapper`
- [x] Implement `__init__(session_id: str, model_name: str = "Qwen/Qwen2.5-Coder-32B-Instruct", api_key: Optional[str] = None)`
    - [x] Call super with "DeepInfra_Qwen2.5-Coder", model name, and "L2"
    - [x] Initialize `openai.AsyncOpenAI` client with DeepInfra base URL
- [x] Implement `async def _execute_internal(task: dict) -> dict`
    - [x] Stream completion
    - [x] Log first 3 chunks as potential reasoning placeholders
    - [x] Log final result and metrics
- [x] Implement `def _parse_thought(chunk: dict) -> Optional[str]`
    - [x] Return `None` (native thinking not exposed yet)
- [x] Implement `def _parse_action(chunk: dict) -> Optional[str]`
    - [x] Return `None`

## Environment Setup
- [x] Ensure `DEEPINFRA_API_KEY` in `.env`
- [x] Install `openai` package

## Test Task
- [x] Verify with prompt: "Refactor this code to use async/await: [simple sync code]"
- [x] Expected: ReasoningPipe file with minimal THOUGHT entries and RESULT
