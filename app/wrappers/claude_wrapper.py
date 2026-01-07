import os
import re
from typing import Optional, Dict
from anthropic import AsyncAnthropic
from app.wrappers.base_wrapper import GravitasAgentWrapper

class ClaudeThinkingWrapper(GravitasAgentWrapper):
    """
    Wrapper for Claude Sonnet 4.5 Thinking models (L3).
    """

    def __init__(self, session_id: str, api_key: Optional[str] = None):
        super().__init__(
            ghost_name="Claude_Thinking",
            session_id=session_id,
            model="claude-sonnet-4-5-thinking",
            tier="L3"
        )
        
        # Configure API key
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key or key == "your_anthropic_key_here":
            raise ValueError("ANTHROPIC_API_KEY must be provided or set as an environment variable.")
        
        self.client = AsyncAnthropic(api_key=key)

    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Model-specific execution for Claude Sonnet 4.5 Thinking.
        """
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Task must include a 'prompt'.")

        # Stream response
        response = await self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            stream=True
        )

        full_output = []
        
        async for chunk in response:
            # 1. Parse and log thoughts (Chain of Thought)
            thought = self._parse_thought(chunk)
            if thought:
                self.pipe.log_thought(thought)
            
            # 2. Extract regular text content
            if hasattr(chunk, 'type') and chunk.type == "content_block_delta":
                if hasattr(chunk.delta, 'text') and chunk.delta.text:
                    full_output.append(chunk.delta.text)

        result_text = "".join(full_output)
        
        # Log final result and metrics
        self.pipe.log_result(
            result=f"Generated {len(result_text)} characters.",
            metrics={
                "tokens": len(result_text) // 4,
                "cost": 0.0  # L3 tier cost tracking placeholder
            }
        )

        return {"output": result_text}

    def _parse_thought(self, chunk) -> Optional[str]:
        """
        Parse <thinking> tags using regex from content block deltas.
        """
        if hasattr(chunk, 'type') and chunk.type == "content_block_delta":
            if hasattr(chunk.delta, 'text') and chunk.delta.text:
                text = chunk.delta.text
                match = re.search(r'<thinking>(.*?)</thinking>', text, re.DOTALL)
                if match:
                    return match.group(1).strip()
        return None

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        """
        Claude doesn't have explicit action markers.
        """
        return None
