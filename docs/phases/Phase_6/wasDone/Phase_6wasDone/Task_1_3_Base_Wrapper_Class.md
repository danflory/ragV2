# Task 1.3: Base Wrapper Class

**File**: `app/wrappers/base_wrapper.py`

## Requirements
- [x] Create abstract base class `GravitasAgentWrapper`
- [x] Implement `__init__(agent_name: str, session_id: str, model: str, tier: str)`
    - [x] Store parameters
    - [x] Initialize `ReasoningPipe`
    - [x] Initialize `SupervisorGuardian`
- [x] Implement `async def execute_task(task: dict) -> dict` (Final method)
    - [x] Notify supervisor of session start
    - [x] Handle permission rejection
    - [x] Call `_execute_internal`
    - [x] Finalize pipe and notify supervisor of completion
    - [x] Return result
- [x] Define `@abstractmethod async def _execute_internal(task: dict) -> dict`
- [x] Define `@abstractmethod def _parse_thought(chunk: dict) -> Optional[str]`
- [x] Define `@abstractmethod def _parse_action(chunk: dict) -> Optional[str]`

## Dependencies
- [x] `from abc import ABC, abstractmethod`
- [x] `from typing import Optional, Dict`
- [x] `from app.lib.reasoning_pipe import ReasoningPipe`
- [x] `from app.services.supervisor.guardian import SupervisorGuardian`

## Test Coverage
- [x] Test that `execute_task` enforces supervisor protocol
- [x] Test that uncertified agent is rejected
- [x] Test that subclass must implement abstract methods
