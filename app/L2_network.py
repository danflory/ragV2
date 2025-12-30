import httpx
import logging
from .interfaces import LLMDriver
from .config import Settings

logger = logging.getLogger("AGY_CLOUD")

class UniversalCloudDriver(LLMDriver):
    """
    The Universal Driver.
    Handles both OpenAI-compatible APIs (DeepInfra/DeepSeek) AND Google Gemini.
    Auto-detects format based on the URL.
    """
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model
        
    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return f"[System Error: Missing API Key for {self.model_name}]"

        # 1. Detect Provider
        is_google = "googleapis.com" in self.base_url

        # 2. Build Headers & Payload accordingly
        if is_google:
            # === GOOGLE GEMINI MODE ===
            url = f"{self.base_url}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7
                }
            }
        else:
            # === OPENAI / DEEPINFRA / DEEPSEEK MODE ===
            url = self.base_url
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a precise and helpful AI."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6
            }

        # 3. Fire the Request
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Cloud Error ({self.model_name}): {response.text}")
                    return f"[API Error {response.status_code}: {response.text}]"

                data = response.json()
                
                # 4. Parse Response (Different paths for Google vs OpenAI)
                if is_google:
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    return data['choices'][0]['message']['content']

        except Exception as e:
            logger.error(f"Connection Exception: {e}")
            return f"[Connection Error: {str(e)}]"

    async def check_health(self) -> bool:
        return bool(self.api_key)