import httpx
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Client for interacting with Google Gemini API via REST.
    Used for L3 (High Intelligence) tasks.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_content(self, model: str, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.api_key:
            logger.error("GOOGLE_API_KEY is missing")
            return {"error": "API Key missing"}

        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": contents
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Gemini API Error: {str(e)}")
                return {"error": str(e)}

    async def test_connection(self) -> bool:
        """Simple Hello World test"""
        contents = [{"parts": [{"text": "Hello"}]}]
        response = await self.generate_content("gemini-1.5-flash", contents)
        return "candidates" in response
