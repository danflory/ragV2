import logging
from google import genai
from .interfaces import LLMDriver

logger = logging.getLogger("Gravitas_L3")

class GoogleGeminiDriver(LLMDriver):
    """
    Driver for Google Gemini (L3 Deep Research).
    Uses the google-genai SDK.
    """
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model_name = model
        self.client = None
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                logger.info(f"✅ L3 Driver Initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI client: {e}")

    async def load_model(self, model_name: str) -> bool:
        """Updates the target model for L3."""
        logger.info(f"🔄 Switching L3 model to: {model_name}")
        self.model_name = model_name
        return True

    async def generate(self, prompt: str) -> str:
        """Generates content using Gemini Pro."""
        if not self.client:
            return "❌ CONFIG ERROR: Gemini API Key missing or client not initialized."

        try:
            # Execute via Async client
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if response and response.text:
                return response.text
            else:
                # Handle safety filters or empty responses
                logger.warning("⚠️ Gemini returned empty or blocked content.")
                return "⚠️ Gemini returned an empty response or content was blocked by safety filters."

        except Exception as e:
            logger.error(f"❌ L3 ERROR: {e}")
            return f"⚠️ L3 UNAVAILABLE: Gemini research failed ({e})"

    async def check_health(self) -> bool:
        """Simple check if client is ready."""
        return self.client is not None and self.api_key is not None
