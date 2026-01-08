import os
import time
import uuid
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.services.registry.ghost_registry import GhostRegistry, GhostSpec
from app.services.registry.shell_registry import ShellRegistry, ModelSpec, ModelTier
from app.services.supervisor.guardian import SupervisorGuardian, AgentNotCertifiedError
from app.services.scheduler.queue import RequestQueue
from app.wrappers.base_wrapper import GravitasAgentWrapper
from app.wrappers.gemini_wrapper import GeminiWrapper
from app.wrappers.claude_wrapper import ClaudeThinkingWrapper
from app.wrappers.deepinfra_wrapper import DeepInfraWrapper
from app.wrappers.ollama_wrapper import OllamaWrapper
from app.services.security.policy_engine import policy_engine
from app.services.security.audit_log import audit_logger, AuditEvent
from app.services.security.deps import get_current_user

logger = logging.getLogger("Gravitas_SUPERVISOR_ROUTER")

# --- Models ---

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    complexity: Optional[int] = 5
    priority: Optional[int] = 10
    force_tier: Optional[str] = None
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 4096

# --- Supervisor Engine ---

class SupervisorEngine:
    """
    Orchestrates routing, certification, and execution.
    """
    def __init__(self):
        self.guardian = SupervisorGuardian()
        self.queue = RequestQueue()
        self.active_workers = 0
        self.max_workers = 5 # Parallelism for L2/L3, L1 is serialized by model lock

    def determine_routing(self, request: ChatCompletionRequest) -> ModelTier:
        """
        Logic from docs/007_model_governance.md
        """
        if request.force_tier:
            return ModelTier(request.force_tier)
        
        # Rule A: Complexity Threshold
        if request.complexity > 8:
            return ModelTier.L3
            
        # Rule B: System Load Protection (Placeholder for telemetry integration)
        # if telemetry.system_load_percent > 90:
        #     return ModelTier.L2
            
        # Rule C: Default Path
        return ModelTier.L1

    def get_wrapper(self, ghost_name: str, shell_name: str, tier: ModelTier, session_id: str) -> GravitasAgentWrapper:
        """
        Returns the appropriate certified wrapper for the given shell.
        """
        from urllib.parse import urlparse, urlunparse
        
        ollama_base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        # Robustly strip path to get base URL
        parsed = urlparse(ollama_base_url)
        ollama_base_url = urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))

        # Strategy 1: Provider-based routing (Preferred)
        shell_spec = ShellRegistry.get_model(shell_name)
        if shell_spec and shell_spec.provider:
            provider = shell_spec.provider.lower()
            if provider == "ollama":
                return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
            elif provider == "google":
                return GeminiWrapper(session_id=session_id)
            elif provider == "anthropic":
                return ClaudeThinkingWrapper(session_id=session_id)
            elif provider == "deepinfra":
                return DeepInfraWrapper(session_id=session_id, model_name=shell_name)

        # Strategy 2: Fallback to Tier + String Matching for unregistered models
        if tier == ModelTier.L1:
            return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
        elif "gemini" in shell_name.lower():
            return GeminiWrapper(session_id=session_id)
        elif "claude" in shell_name.lower():
            return ClaudeThinkingWrapper(session_id=session_id)
        elif tier == ModelTier.L2:
            return DeepInfraWrapper(session_id=session_id, model_name=shell_name)
        
        raise ValueError(f"No wrapper found for {shell_name} at tier {tier}")

    async def process_chat(self, request: ChatCompletionRequest, user_payload: Dict[str, Any]):
        """
        The main processing flow.
        """
        session_id = str(uuid.uuid4())
        
        # 1. Routing Decision
        target_tier = self.determine_routing(request)
        
        # 2. Identity Resolution
        # Trust the token subject as the Ghost Identity.
        # Fallbacks are only for AUTH_DISABLED mode (handled by get_current_user).
        ghost_name = user_payload.get("sub", "Supervisor_Managed_Agent")
        
        # 'request.model' specifies the TARGET execution shell (e.g. "gemma2:27b")
        # However, if the user requested a Ghost Name as the model (e.g. "Librarian"),
        # we resolve that to their preferred shell.
        
        target_ghost = GhostRegistry.get_ghost(request.model)
        if target_ghost:
            # User asked for "Librarian" -> resolve to "llama3:70b"
            shell_name = target_ghost.preferred_shell
        else:
            # User asked for "gemma2:27b" -> use as is
            shell_name = request.model

        # 2.5 Security Check (Phase 7)
        if not policy_engine.check_permission(ghost_name, "execute", shell_name):
            await audit_logger.log_event(AuditEvent(
                ghost_id=ghost_name,
                shell_id=shell_name,
                action="execute",
                resource=shell_name,
                result="DENIED",
                reason="Insufficient permissions for this shell"
            ))
            raise HTTPException(status_code=403, detail=f"Ghost '{ghost_name}' is not authorized to execute shell '{shell_name}'")

        # 3. Wrapper Initialization
        try:
            wrapper = self.get_wrapper(ghost_name, shell_name, target_tier, session_id)
        except Exception as e:
            logger.error(f"Failed to create wrapper: {e}")
            raise HTTPException(status_code=400, detail=str(e))

        # 4. Certification Check (Implicit in execute_task, but we should be aware)
        # and Queue Submission
        # Note: True queuing logic for L1 (shared VRAM) would involve a worker loop
        # For this implementation, we'll execute it and let guardian handle session tracking.
        
        logger.info(f"Routing {ghost_name} to {shell_name} ({target_tier.value})")
        
        try:
            # We wrap the internal execution to match our spec's task format
            task = {"prompt": request.messages[-1]["content"], "messages": request.messages}
            result = await wrapper.execute_task(task)
            
            # Audit success
            await audit_logger.log_event(AuditEvent(
                ghost_id=ghost_name,
                shell_id=shell_name,
                action="execute",
                resource=shell_name,
                result="SUCCESS"
            ))
            
            # Format to OpenAI response
            return {
                "id": f"chatcmpl-{session_id}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": shell_name,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": result.get("output", "")
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
        except AgentNotCertifiedError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# --- API Router ---

router = APIRouter()
engine = SupervisorEngine()

@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, user: Dict = Depends(get_current_user)):
    return await engine.process_chat(request, user)


