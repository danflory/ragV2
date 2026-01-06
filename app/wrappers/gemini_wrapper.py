import os
import google.generativeai as genai
from typing import Optional, Dict, List
from app.wrappers.base_wrapper import GravitasAgentWrapper

class GeminiWrapper(GravitasAgentWrapper):
    """
    Wrapper for Gemini 2.0 Flash Thinking models (L3).
    """

    def __init__(self, session_id: str, api_key: Optional[str] = None):
        super().__init__(
            agent_name="Gemini_Thinking",
            session_id=session_id,
            model="gemini-2.0-flash-thinking-exp",
            tier="L3"
        )
        
        # Configure API key
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError("GOOGLE_API_KEY must be provided or set as an environment variable.")
        
        genai.configure(api_key=key)
        self.client = genai.GenerativeModel(self.model)

    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Model-specific execution for Gemini 2.0 Flash Thinking.
        """
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Task must include a 'prompt'.")

        # Start streaming response
        # Note: generate_content_async with stream=True returns an AsyncGenerateContentResponse
        response = await self.client.generate_content_async(
            prompt,
            stream=True
        )

        full_output = []
        
        # Iterate over the async stream
        async for chunk in response:
            # 1. Parse and log thoughts (Chain of Thought)
            thought = self._parse_thought(chunk)
            if thought:
                self.pipe.log_thought(thought)
            
            # 2. Extract regular text content
            if hasattr(chunk, 'text') and chunk.text:
                full_output.append(chunk.text)

        result_text = "".join(full_output)
        
        # Log final result and metrics
        # We estimate tokens as length / 4 for now as Gemini 2.0 doesn't always return token counts in stream chunks
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
        Extract the 'thinking' field from a Gemini response chunk.
        """
        # In Gemini 2.0 Flash Thinking, thinking process is in 'parts' with a specific trait
        # but often exposed directly in the experimental SDK as 'thinking'
        if hasattr(chunk, 'candidates') and chunk.candidates:
            candidate = chunk.candidates[0]
            if hasattr(candidate, 'content') and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'thought') and part.thought:
                        return part.text
                    # Check for parts that are specifically marked as thinking
                    # Note: SDK versions vary, but often 'thought' boolean or 'thinking' property
                    if getattr(part, 'thought', False):
                        return part.text
        
        # Fallback for different SDK versions or experimental features
        if hasattr(chunk, 'thinking'):
            return chunk.thinking
            
        return None

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        """
        Gemini doesn't have explicit action markers in the standard response yet.
        """
        return None
