import httpx
import logging
from .interfaces import LLMDriver

logger = logging.getLogger("AGY_L2")

class DeepInfraDriver(LLMDriver):
    """
    Dedicated Driver for DeepInfra (L2 Reasoning Layer).
    Strictly follows OpenAI-compatible API format.
    """
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model
        
    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[Config Error: DeepInfra API Key missing]"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # DeepInfra / OpenAI Standard Payload
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a precise Senior Python Engineer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2, # Low temp for coding precision
            "max_tokens": 2048
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.base_url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    error_msg = f"DeepInfra Error {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    return f"[{error_msg}]"

                data = response.json()
                return data['choices'][0]['message']['content']

        except Exception as e:
            logger.error(f"L2 Connection Failed: {e}")
            return f"[L2 Connection Error: {str(e)}]"

    async def check_health(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 10