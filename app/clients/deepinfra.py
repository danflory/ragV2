import httpx
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DeepInfraClient:
    """
    Client for interacting with DeepInfra's OpenAI-compatible API.
    Used for L2 (Network/Cloud) offloading.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPINFRA_API_KEY")
        self.base_url = "https://api.deepinfra.com/v1/openai/chat/completions"

    async def chat_completion(self, model: str, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        if not self.api_key:
            logger.error("DEEPINFRA_API_KEY is missing")
            return {"error": "API Key missing", "fallback_content": "DeepInfra not configured"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"DeepInfra API Error: {str(e)}")
                return {"error": str(e)}

    async def test_connection(self) -> bool:
        """Simple Hello World test"""
        messages = [{"role": "user", "content": "Hello"}]
        # Llama 3 70b is a common model on DeepInfra
        response = await self.chat_completion("meta-llama/Meta-Llama-3-70B-Instruct", messages)
        return "choices" in response
