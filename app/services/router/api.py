import os
import time
import uuid
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

# Imports adapted for Router service structure
from app.services.registry.ghost_registry import GhostRegistry
from app.services.registry.shell_registry import ShellRegistry, ModelTier
from app.services.router.guardian_client import GuardianClient, AgentNotCertifiedError
# Queue might need to be abstracted if we want true separation, 
# but for now we can rely on a local internal queue or ignore it since Router is stateless scaling unit.
# Supervisor had RequestQueue. Let's keep a simplified internal queue if needed, or remove if unused.
# Supervisor used queue for "active_workers" limit.
# Let's remove Queue for now to simplify, assuming Router scales horizontally.
# But allow basic L1 locking if needed.
# For API compatibility, we keep logic similar.

from app.services.router.gatekeeper_client import gatekeeper_client
from app.services.router.wrappers.base_wrapper import GravitasAgentWrapper
from app.services.router.wrappers.gemini_wrapper import GeminiWrapper
from app.services.router.wrappers.claude_wrapper import ClaudeThinkingWrapper
from app.services.router.wrappers.deepinfra_wrapper import DeepInfraWrapper
from app.services.router.wrappers.ollama_wrapper import OllamaWrapper

logger = logging.getLogger("Gravitas_ROUTER_API")

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    complexity: Optional[int] = 5
    priority: Optional[int] = 10
    force_tier: Optional[str] = None
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 4096

class RouterEngine:
    def __init__(self):
        self.guardian = GuardianClient(fallback_to_local=False)
        # self.queue = ... # Removed
        self.active_workers = 0

    def determine_routing(self, request: ChatCompletionRequest) -> ModelTier:
        if request.force_tier:
            return ModelTier(request.force_tier)
        if request.complexity > 8:
            return ModelTier.L3
        return ModelTier.L1

    def get_wrapper(self, ghost_name: str, shell_name: str, tier: ModelTier, session_id: str) -> GravitasAgentWrapper:
        from urllib.parse import urlparse, urlunparse
        
        ollama_base_url = os.getenv("OLLAMA_URL", "http://gravitas_ollama:11434") # Use service name default
        
        parsed = urlparse(ollama_base_url)
        ollama_base_url = urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))

        shell_spec = ShellRegistry.get_model(shell_name)
        if shell_spec and shell_spec.provider:
            provider = shell_spec.provider.lower()
            if provider == "ollama":
                # Only L1 needs internal OLLAMA_URL. External providers use public APIs.
                return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
            elif provider == "google":
                return GeminiWrapper(session_id=session_id)
            elif provider == "anthropic":
                return ClaudeThinkingWrapper(session_id=session_id)
            elif provider == "deepinfra":
                return DeepInfraWrapper(session_id=session_id, model_name=shell_name)

        # Fallback
        if tier == ModelTier.L1:
            return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
        elif "gemini" in shell_name.lower():
            return GeminiWrapper(session_id=session_id)
        elif "claude" in shell_name.lower():
            return ClaudeThinkingWrapper(session_id=session_id)
        elif tier == ModelTier.L2:
            return DeepInfraWrapper(session_id=session_id, model_name=shell_name)
        
        raise ValueError(f"No wrapper found for {shell_name}")

    async def process_chat(self, request: ChatCompletionRequest, authorization: str):
        session_id = str(uuid.uuid4())
        
        # 1. Routing
        target_tier = self.determine_routing(request)
        target_ghost = GhostRegistry.get_ghost(request.model)
        if target_ghost:
            shell_name = target_ghost.preferred_shell
        else:
            shell_name = request.model
            
        # 2. Gatekeeper Check
        if not authorization:
            if os.getenv("AUTH_DISABLED", "false").lower() == "true":
                 logger.warning("Auth disabled: Skipping Gatekeeper validation")
                 # Use a generic name that MIGHT be certified if we use a wrapper that ignores it,
                 # BUT for L1/L2 routing, the wrappers use their OWN names (e.g. Ollama_codellama_7b).
                 # So this name 'Anonymous' is mostly for logging/routing decision context in RouterEngine.
                 # Wait, 'ghost_name' from here is PASSED to get_wrapper.
                 # But get_wrapper (Step 332) DOES NOT use it for Ollama/DeepInfra/Gemini wrappers!
                 # It calls constructor WITHOUT ghost_name.
                 # So the wrapper uses its HARDCODED name.
                 # exception: OllamaWrapper uses f"Ollama_{model_name}".
                 # So changing "Anonymous" to "Supervisor_Managed_Agent" WON'T HELP if the Wrapper ignores it.
                 ghost_name = "Supervisor_Managed_Agent"
                 # Skip to execution
            else:
                 raise HTTPException(status_code=401, detail="Missing Authorization header")
        else:
            token = authorization.replace("Bearer ", "") if authorization else ""
            metadata = {"shell_id": shell_name, "routing_tier": target_tier.value}
            
            validation = await gatekeeper_client.validate_request(
                token=token, 
                action="execute", 
                resource=shell_name, 
                metadata=metadata
            )
            
            if not validation["allowed"]:
                raise HTTPException(status_code=validation.get("error_code", 403), detail=validation.get("detail", "Access denied"))
                
            ghost_name = validation.get("ghost_id", "Unknown")

        # 3. Execution
        try:
            wrapper = self.get_wrapper(ghost_name, shell_name, target_tier, session_id)
            logger.info(f"Routing {ghost_name} to {shell_name}")
            
            task = {"prompt": request.messages[-1]["content"], "messages": request.messages}
            result = await wrapper.execute_task(task)
            
            logger.info(f"Execution successful for {ghost_name} on {shell_name}")
            
            return {
                "id": f"chatcmpl-{session_id}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": shell_name,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": result.get("output", "")},
                    "finish_reason": "stop"
                }]
            }
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

router = APIRouter()
engine = RouterEngine()

@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, authorization: Optional[str] = Header(None)):
    return await engine.process_chat(request, authorization)

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "router"}
