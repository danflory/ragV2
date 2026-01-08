# Task 2.2: Claude Sonnet 4.5 Thinking Wrapper

**File**: `app/wrappers/claude_wrapper.py`

## Requirements
- [x] Inherit from `GravitasAgentWrapper`
- [x] Implement `__init__(session_id: str, api_key: Optional[str] = None)`
    - [x] Call super with "Claude_Thinking", "claude-sonnet-4-5-thinking", "L3"
    - [x] Initialize `anthropic.AsyncAnthropic` client
- [x] Implement `async def _execute_internal(task: dict) -> dict`
    - [x] Extract prompt
    - [x] Stream response with `<thinking>` tag parsing
    - [x] Log thoughts to pipe
    - [x] Log final result and metrics
- [x] Implement `def _parse_thought(chunk: dict) -> Optional[str]`
    - [x] Parse `<thinking>` tags using regex from content block deltas
- [x] Implement `def _parse_action(chunk: dict) -> Optional[str]`
    - [x] Return `None`

## Environment Setup
- [x] Ensure `ANTHROPIC_API_KEY` in `.env`
- [x] Install `anthropic` package

## Test Task
- [x] Verify with prompt: "Analyze the theological significance of 'gravitas'"
- [x] Expected: ReasoningPipe file with THOUGHT entries from `<thinking>` tags
