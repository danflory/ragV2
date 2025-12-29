import logging
import httpx
from datetime import datetime
from .config import config
from .interfaces import LLMDriver

logger = logging.getLogger("AGY_L1")

class L1Driver(LLMDriver):
    """
    Modern L1 Driver for AntiGravity.
    Refactored for SOLID/IoC:
    1. Inherits from LLMDriver (Interface)
    2. Accepts config via constructor (Dependency Injection)
    3. Uses direct HTTPX for robust WSL networking
    """
    def __init__(self, base_url: str, model_name: str):
        self.last_success = datetime.now()
        # Dependency Injection: Store the config passed in, don't read global config
        self.base_url = base_url.rstrip("/")
        self.model = model_name

    async def check_health(self) -> bool:
        """
        Implementation of LLMDriver.check_health
        Verifies model availability using raw HTTP.
        """
        try:
            async with httpx.AsyncClient() as client:
                # 1. Hit the API tags endpoint directly
                response = await client.get(f"{self.base_url}/api/tags")
                
                if response.status_code != 200:
                    logger.error(f"❌ Ollama API returned status {response.status_code}")
                    return False

                # 2. Parse JSON
                data = response.json()
                models_list = data.get("models", [])
                installed_names = [m.get("name") for m in models_list]
                
                # 3. Check for match using injected model name
                if self.model in installed_names:
                    return True
                
                # Handle 'latest' tag implication
                for name in installed_names:
                    if name and name.startswith(self.model.split(':')[0]):
                        return True

                logger.error(f"❌ Model '{self.model}' not found. Available: {installed_names}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Connection to Ollama failed: {e}")
            return False

    async def generate(self, prompt: str) -> str:
        """
        Implementation of LLMDriver.generate
        """
        # Verification step
        if not await self.check_health():
            return "ESCALATE TO L2"

        try:
            # We still access config.USER_NAME for the prompt context, 
            # as that is session data, not infrastructure config.
            logger.info(f"🐢 L1 [{self.model}] processing for {config.USER_NAME}...")
            
            system_msg = f"You are an expert AI assistant helping {config.USER_NAME}."
            
            payload = {
                "model": self.model,  # Use injected model
                "prompt": prompt,
                "system": system_msg,
                "stream": False,
                "options": {
                    "num_ctx": 4096,
                    "temperature": 0.7,
                    "num_gpu": 1  # Force TITAN RTX usage
                }
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                
                if response.status_code != 200:
                    logger.warning(f"⚠️ L1 API Error: {response.text}. Escalating...")
                    return "ESCALATE TO L2"

                data = response.json()
                self.last_success = datetime.now()
                return data.get("response", "")

        except Exception as e:
            logger.error(f"🔥 L1 Critical Failure: {e}")
            return "ESCALATE TO L2"

    # --- Backward Compatibility for existing Router ---
    # These alias the new methods to the old names so router.py doesn't break
    async def ask_local_llm(self, prompt: str) -> str:
        return await self.generate(prompt)

    async def check_model_exists(self) -> bool:
        return await self.check_health()

# --- Singleton Instantiation (The "Glue") ---
# We manually inject the config here. In the future, a Container will do this.
l1_engine = L1Driver(base_url=config.OLLAMA_BASE_URL, model_name=config.MODEL)