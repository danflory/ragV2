# Task 2.1: Gemini 2.0 Flash Thinking Wrapper

**File**: `app/wrappers/gemini_wrapper.py`

## Requirements
- [x] Inherit from `GravitasAgentWrapper`
- [x] Implement `__init__(session_id: str, api_key: Optional[str] = None)`
    - [x] Call super with "Gemini_Thinking", "gemini-2.0-flash-thinking-exp", "L3"
    - [x] Initialize `google.generativeai` client
- [x] Implement `async def _execute_internal(task: dict) -> dict`
    - [x] Extract prompt
    - [x] Stream response and parse thoughts
    - [x] Log thoughts to pipe
    - [x] Log final result and metrics
- [x] Implement `def _parse_thought(chunk: dict) -> Optional[str]`
    - [x] Extract `thinking` field from Gemini chunk
- [x] Implement `def _parse_action(chunk: dict) -> Optional[str]`
    - [x] Return `None` (no explicit actions yet)

## Environment Setup
- [x] Ensure `GOOGLE_API_KEY` in `.env`
- [x] Install `google-generativeai` package

## Test Task
- [x] Verify with prompt: "Explain the concept of 'gravitas' in one paragraph"
- [x] Expected: ReasoningPipe file with THOUGHT entries
