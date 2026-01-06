# Gravitas Wrapper Development Guide

## Introduction
In Gravitas Phase 6 (Reasoning Pipes), all agents must be "wrapped" to standardize how they log thoughts, actions, and results. This ensures that the Supervisor can enforce quality control and audit agent performance. 

**Key Requirement**: Before any agent can execute in the production environment, its wrapper must be **Certified** by the Supervisor.

## Quick Start
To create a new agent wrapper, create a python file in `app/wrappers/` (e.g., `my_agent_wrapper.py`).

### Template Code
```python
from typing import Dict, Optional
from app.wrappers.base_wrapper import GravitasAgentWrapper

class MyNewAgentWrapper(GravitasAgentWrapper):
    def __init__(self, session_id: str):
        super().__init__(
            agent_name="MyNewAgent",
            session_id=session_id,
            model="my-model-name",
            tier="L1" # L1 (Local), L2 (Specialized), or L3 (Frontier)
        )
        # Initialize your model client here

    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Your model's execution logic goes here.
        """
        prompt = task.get("prompt")
        
        # ... call your model API ...
        
        # LOGGING IS MANDATORY:
        self.pipe.log_thought("Thinking about the prompt...")
        
        # ... parsing response ...
        
        self.pipe.log_result(
            result="Final answer",
            metrics={"tokens": 100, "cost": 0.0}
        )
        
        return {"output": "Final answer"}

    def _parse_thought(self, chunk: Dict) -> Optional[str]:
        # Extract chain-of-thought from model chunk
        return None

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        # Extract action declaration from model chunk
        return None
```

## Step-by-Step Tutorial

### 1. Inheritance
All wrappers must inherit from `GravitasAgentWrapper`. This base class handles the communication with the `SupervisorGuardian` and manages the `ReasoningPipe` lifecycle.

### 2. Method Overrides
You must implement three abstract methods:
*   `_execute_internal(self, task: Dict) -> Dict`: The core logic. You **must** call `self.pipe.log_thought()`, `self.pipe.log_action()`, and `self.pipe.log_result()`.
*   `_parse_thought(self, chunk: Dict) -> Optional[str]`: Helper to extract reasoning text from streaming chunks.
*   `_parse_action(self, chunk: Dict) -> Optional[str]`: Helper to extract tool usage or actions.

### 3. Local Testing
Create a simple script to run your wrapper:
```python
import asyncio
from app.wrappers.my_agent_wrapper import MyNewAgentWrapper

async def test():
    agent = MyNewAgentWrapper(session_id="test-session-001")
    result = await agent.execute_task({"prompt": "Hello"})
    print(result)

if __name__ == "__main__":
    asyncio.run(test())
```

### 4. Certification
Once your wrapper is ready, you must certify it. The Certifier performs static analysis and dynamic testing.

```bash
python app/services/supervisor/certifier.py --certify app/wrappers/my_agent_wrapper.py --agent-name MyNewAgent
```
If successful, a certificate file will be created in `app/.certificates/MyNewAgent.json`.

## Best Practices

*   **Error Handling**: Wrap external API calls in try/except blocks. If an error occurs, the base class will attempt to save whatever reasoning chain was captured before the crash.
*   **Timeout Management**: Use `asyncio.wait_for` for model calls to prevent hanging processes.
*   **Cost Tracking**: Estimate or calculate exact costs in `log_result`.
*   **Reasoning Clarity**: Ensure that `log_thought` captures *internal monologue*, not just the final output.

## Troubleshooting

*   **Static Analysis Failed**: Ensure you import the base class correctly and have all required methods defined.
*   **Dynamic Test Failed**: The certifier runs a "dry run". Ensure your wrapper can handle a basic prompt without crashing.
*   **"Agent not certified" Error**: You tried to run `execute_task` without a valid certificate in `app/.certificates/`. Run the certifier script.
