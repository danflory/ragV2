# Task 1.1: ReasoningPipe Standard Library

**File**: `app/lib/reasoning_pipe.py`

## Requirements
- [x] Create `ReasoningPipe` class
- [x] Implement `__init__(agent_name: str, session_id: str, model: str, tier: str)`
    - [x] Initialize session metadata
    - [x] Create buffer for in-memory logging
    - [x] Generate output path: `docs/journals/ReasoningPipe_{agent_name}_{session_id}.md`
- [x] Implement `log_thought(content: str, timestamp: Optional[datetime] = None) -> None`
    - [x] Append to buffer: `**[HH:MM:SS.mmm]** THOUGHT: {content}`
    - [x] Auto-generate timestamp if not provided (use `datetime.now()`)
    - [x] Validate content is non-empty string
- [x] Implement `log_action(action: str, details: Optional[dict] = None) -> None`
    - [x] Append to buffer: `**[HH:MM:SS.mmm]** ACTION: {action}`
    - [x] Format details if provided: `ACTION: {action} (key1: val1, key2: val2)`
- [x] Implement `log_result(result: str, metrics: Optional[dict] = None) -> None`
    - [x] Append to buffer: `**[HH:MM:SS.mmm]** RESULT: {result}`
    - [x] Store metrics for session metadata (tokens, duration, cost)
- [x] Implement `finalize() -> Path`
    - [x] Write buffer to file with full markdown template
    - [x] Append summary line to `docs/journals/ReasoningPipe_{agent_name}.md`
    - [x] Return Path to written file
    - [x] Clear buffer after write

## Markdown Template
- [x] Use exact template format:
```markdown
# ReasoningPipe: {agent_name} | Session: {session_id}

**Started**: {ISO8601_timestamp}  
**Model**: {model_name}  
**Tier**: {L1|L2|L3}  
**Task**: {task_description if provided}

---

## Thought Stream

{buffer_contents_here}

---

## Session Metadata

**Duration**: {duration}s  
**Tokens Generated**: {tokens}  
**Efficiency**: {tokens_per_second} tok/s  
**Cost**: ${cost} ({tier})  
**Finalized**: {ISO8601_timestamp}
```

## Error Handling
- [x] Ensure `docs/journals/` existence
- [x] Raise `ReasoningPipeWriteError` on failure
- [x] Handle double `finalize()` calls with warning

## Dependencies
- [x] `from datetime import datetime`
- [x] `from pathlib import Path`
- [x] `from typing import Optional, Dict`
- [x] `import json`

## Test Coverage
- [x] Test each method independently
- [x] Test full workflow: init → log_thought → log_action → log_result → finalize
- [x] Test timestamp auto-generation
- [x] Test file creation in `docs/journals/`
- [x] Test error handling (write failures, double finalize)
