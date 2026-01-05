import httpx
import logging
import GPUtil
from .interfaces import LLMDriver
from .config import Settings
from .telemetry import telemetry
from .exceptions import OverloadError

logger = logging.getLogger("Gravitas_L1")

class LocalLlamaDriver(LLMDriver):
    def __init__(self, config: Settings):
        self.base_url = config.L1_URL
        self.model_name = config.L1_MODEL
        self.timeout = 60.0

    async def load_model(self, model_name: str) -> bool:
        """Switches the active model and ensures it is available."""
        logger.info(f"🔄 Switching L1 model to: {model_name}")
        self.model_name = model_name
        return await self.ensure_model()

    async def generate(self, prompt: str) -> str:
        # Check VRAM before generation to prevent overload
        await self.check_vram()
        url = f"{self.base_url}/api/generate"
        
        # === SYSTEM INSTRUCTION ===
        # We wrap the user prompt to teach L1 about its new tool.
        system_prompt = (
            "You are the Gravitas Assistant. You are a helpful, conversational coding expert.\n"
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

    async def check_vram(self) -> dict:
        """
        Check VRAM usage and implement overload protection.
        
        Returns:
            dict: VRAM information including total, used, and free memory per GPU
            
        Raises:
            OverloadError: If free VRAM is less than 2GB on any GPU
        """
        try:
            gpus = GPUtil.getGPUs()
            vram_info = []
            
            for gpu in gpus:
                total_vram = gpu.memoryTotal / 1024  # Convert to GB
                used_vram = gpu.memoryUsed / 1024
                free_vram = gpu.memoryFree / 1024
                
                gpu_info = {
                    'id': gpu.id,
                    'total_gb': round(total_vram, 2),
                    'used_gb': round(used_vram, 2),
                    'free_gb': round(free_vram, 2)
                }
                vram_info.append(gpu_info)
                
                # Log VRAM check
                await telemetry.log(
                    event_type="VRAM_CHECK",
                    component="L1",
                    value=free_vram,
                    metadata={
                        'gpu_id': gpu.id,
                        'total_vram_gb': total_vram,
                        'used_vram_gb': used_vram
                    },
                    status="OK"
                )
                
                # Check for overload condition
                if free_vram < 2.0:  # Less than 2GB free
                    await telemetry.log(
                        event_type="VRAM_LOCKOUT",
                        component="L1",
                        value=free_vram,
                        metadata={
                            'gpu_id': gpu.id,
                            'total_vram_gb': total_vram,
                            'used_vram_gb': used_vram
                        },
                        status="ERROR"
                    )
                    raise OverloadError(
                        message=f"VRAM overload detected on GPU {gpu.id}: {free_vram:.2f}GB free < 2GB threshold",
                        resource_type="VRAM",
                        current_value=free_vram,
                        threshold=2.0
                    )
            
            return vram_info
            
        except OverloadError:
            # Re-raise overload errors
            raise
        except Exception as e:
            logger.error(f"❌ VRAM CHECK FAILED: {e}")
            # Don't raise exception for monitoring failures, just log and continue
            return []
