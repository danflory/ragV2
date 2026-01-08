import json
import re
import httpx
from typing import Optional, Dict
from app.services.router.wrappers.base_wrapper import GravitasAgentWrapper

class OllamaWrapper(GravitasAgentWrapper):
    """
    Wrapper for Ollama local models (L1).
    Supports any model available in the local Ollama instance.
    """

    def __init__(self, session_id: str, model_name: str, ollama_url: str = "http://localhost:11434"):
        super().__init__(
            ghost_name=f"Ollama_{model_name.replace(':', '_')}",
            session_id=session_id,
            model=model_name,
            tier="L1"
        )
        self.ollama_url = ollama_url

    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Model-specific execution for Ollama API.
        """
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Task must include a 'prompt'.")

        full_output = []
        last_chunk = {}

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True}
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise RuntimeError(f"Ollama API error ({response.status_code}): {error_text.decode()}")

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    last_chunk = chunk
                    
                    # 1. Parse and log thoughts (Chain of Thought)
                    thought = self._parse_thought(chunk)
                    if thought:
                        self.pipe.log_thought(thought)
                    
                    # 2. Parse and log actions
                    action = self._parse_action(chunk)
                    if action:
                        self.pipe.log_action(action)
                    
                    # 3. Extract regular text content
                    text = chunk.get("response", "")
                    if text:
                        full_output.append(text)
                    
                    if chunk.get("done"):
                        break

        result_text = "".join(full_output)
        
        # Log final result and metrics
        tokens = last_chunk.get("eval_count", 0)  # eval_count is tokens generated
        if tokens == 0:
            tokens = len(result_text) // 4 # Fallback
            
        self.pipe.log_result(
            result=f"Generated {len(result_text)} characters.",
            metrics={
                "tokens": tokens,
                "cost": 0.0  # L1 tier (local) cost is 0
            }
        )

        return {"output": result_text}

    def _parse_thought(self, chunk: Dict) -> Optional[str]:
        """
        Parse custom <think> tags from the response field in chunk.
        """
        text = chunk.get("response", "")
        if not text:
            return None
            
        match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        """
        Parse custom <action> tags from the response field in chunk.
        """
        text = chunk.get("response", "")
        if not text:
            return None
            
        match = re.search(r'<action>(.*?)</action>', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
