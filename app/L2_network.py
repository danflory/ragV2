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
        
    async def load_model(self, model_name: str) -> bool:
        """Updates the target model for L2."""
        logger.info(f"🔄 Switching L2 model to: {model_name}")
        self.model_name = model_name
        return True

    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "❌ CONFIG ERROR: DeepInfra API Key missing in `.env`."

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

        # RETRY CONFIG
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(self.base_url, headers=headers, json=payload)
                    
                    # 1. Success
                    if response.status_code == 200:
                        data = response.json()
                        
                        # --- STATS CAPTURE ---
                        from .database import db
                        usage = data.get("usage", {})
                        await db.log_usage(
                            model=self.model_name,
                            layer="L2",
                            prompt_tokens=usage.get("prompt_tokens", 0),
                            completion_tokens=usage.get("completion_tokens", 0),
                            duration_ms=0 
                        )
                        return data['choices'][0]['message']['content']

                    # 2. Fatal Errors (Auth / Bad Request) - Do not retry
                    if 400 <= response.status_code < 500:
                        error_msg = f"L2 CLIENT ERROR {response.status_code}: {response.text}"
                        logger.error(error_msg)
                        return f"⚠️ {error_msg}"
                    
                    # 3. Server Errors (5xx) - Retry
                    logger.warning(f"⚠️ L2 RETRY {attempt+1}/{max_retries}: Server Error {response.status_code}")

            except httpx.RequestError as e:
                # 4. Connection Failures - Retry
                logger.warning(f"⚠️ L2 RETRY {attempt+1}/{max_retries}: Connection Failed ({e})")
            
            # Backoff for next attempt (only if we haven't exhausted retries)
            if attempt < max_retries - 1:
                import asyncio
                await asyncio.sleep(base_delay * (2 ** attempt)) # 1s, 2s, 4s...

        # Final Failure
        logger.error("❌ L2 FAILED after all retries.")
        return "⚠️ L2 UNAVAILABLE: Connection to DeepInfra reasoning layer failed after multiple retries. Please check your internet connection."

    async def check_health(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 10