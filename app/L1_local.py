import httpx
import logging
from .interfaces import LLMDriver
from .config import Settings

logger = logging.getLogger("AGY_L1")

class LocalLlamaDriver(LLMDriver):
    def __init__(self, config: Settings):
        self.base_url = config.L1_URL
        self.model_name = config.L1_MODEL
        self.timeout = 60.0

    async def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        
        # === SYSTEM INSTRUCTION ===
        # We wrap the user prompt to teach L1 about its new tool.
        system_prompt = (
            "You are the AntiGravity Assistant. You are a helpful, conversational coding expert.\n"
            "--- COMMANDS ---\n"
            "- To save work: <reflex action=\"git_sync\" />\n"
            "- To ESCALATE: If the user types '\\L2' at the start of their message or asks a deep logic/math question, reply ONLY with the word ESCALATE.\n"
            "--- BEHAVIOR ---\n"
            "For general questions like 'hello' or greetings, respond normally and do NOT include tags.\n\n"
            f"Context:\n{prompt}"
        )

        payload = {
            "model": self.model_name,
            "prompt": system_prompt, 
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    return f"[L1 Error: {response.status_code}]"

                data = response.json()
                raw_response = data.get("response", "").strip()
                
                # --- STATS CAPTURE ---
                from .database import db
                prompt_tokens = data.get("prompt_eval_count", 0)
                completion_tokens = data.get("eval_count", 0)
                # Ollama duration is in nanoseconds
                duration_ms = data.get("total_duration", 0) // 1_000_000 
                
                await db.log_usage(
                    model=self.model_name,
                    layer="L1",
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    duration_ms=duration_ms
                )
                
                # Cleanup: Sometimes 7b models add extra spaces or quotes
                if '<reflex action="git_sync"' in raw_response:
                    return '<reflex action="git_sync" />'
                
                return raw_response

        except Exception as e:
            return f"[L1 Error: {str(e)}]"

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(self.base_url)
                return resp.status_code == 200
        except:
            return False

    async def ensure_model(self) -> bool:
        """Checks if model exists, if not, pulls it."""
        check_url = f"{self.base_url}/api/tags"
        pull_url = f"{self.base_url}/api/pull"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Check if exists
                resp = await client.get(check_url)
                if resp.status_code == 200:
                    models_data = resp.json().get('models')
                    if models_data:
                        models = [m['name'] for m in models_data]
                        if self.model_name in models or f"{self.model_name}:latest" in models:
                            logger.info(f"✅ Model {self.model_name} already present.")
                            return True
                
                # 2. Pull if missing
                logger.info(f"📥 Pulling model {self.model_name} (this may take a while)...")
                await client.post(pull_url, json={"name": self.model_name, "stream": False}, timeout=300.0)
                return True
        except Exception as e:
            logger.error(f"❌ Failed to ensure model: {e}")
            return False