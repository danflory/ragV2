import os
import logging
from typing import Optional, Dict
from openai import AsyncOpenAI
from app.wrappers.base_wrapper import GravitasAgentWrapper

logger = logging.getLogger(__name__)

class DeepInfraWrapper(GravitasAgentWrapper):
    """
    Wrapper for DeepInfra models, specifically Qwen2.5-Coder (L2).
    Uses the OpenAI-compatible SDK provided by DeepInfra.
    """

    def __init__(self, session_id: str, model_name: str = "Qwen/Qwen2.5-Coder-32B-Instruct", api_key: Optional[str] = None):
        super().__init__(
            agent_name="DeepInfra_Qwen2.5-Coder",
            session_id=session_id,
            model=model_name,
            tier="L2"
        )
        
        # Configure API key
        key = api_key or os.getenv("DEEPINFRA_API_KEY")
        if not key or key == "your_deepinfra_key_here":
            # Fallback to L2_KEY if present
            key = os.getenv("L2_KEY")
            
        if not key:
            raise ValueError("DEEPINFRA_API_KEY (or L2_KEY) must be provided or set as an environment variable.")
        
        self.client = AsyncOpenAI(
            api_key=key,
            base_url="https://api.deepinfra.com/v1/openai"
        )

    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Model-specific execution for DeepInfra (OpenAI-compatible).
        """
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Task must include a 'prompt'.")

        # Stream response
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=4096
        )

        full_output = []
        chunk_count = 0
        
        async for chunk in response:
            if not chunk.choices:
                continue
                
            delta = chunk.choices[0].delta
            content = delta.content
            
            if content:
                # 1. Log first 3 chunks as potential reasoning placeholders
                # Note: For non-thinking models, we just provide a trace of the start
                if chunk_count < 3:
                    self.pipe.log_thought(f"Processing: {content.strip()[:50]}...")
                
                full_output.append(content)
                chunk_count += 1

        result_text = "".join(full_output)
        
        # Log final result and metrics
        # We estimate tokens as length / 4 for now
        self.pipe.log_result(
            result=f"Generated {len(result_text)} characters.",
            metrics={
                "tokens": len(result_text) // 4,
                "cost": 0.0  # L2 tier cost tracking placeholder
            }
        )

        return {"output": result_text}

    def _parse_thought(self, chunk: Dict) -> Optional[str]:
        """
        DeepInfra doesn't expose native thinking output yet.
        Placeholder for future reasoning-capable models on DeepInfra.
        """
        return None

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        """
        DeepInfra doesn't have action markers in standard completion.
        """
        return None
