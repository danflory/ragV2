import httpx
import os
import logging
from typing import Optional, Dict

# Fallback imports
from app.services.security.auth import decode_access_token
from app.services.security.policy_engine import policy_engine
# Audit logger fallback is tricky because it's async fire-and-forget, 
# but for local fallback we might skip or use the local one.
# Given the plan says "Duplicate security logic", we can use the local modules.
from app.services.security.audit_log import audit_logger, AuditEvent

logger = logging.getLogger("Gravitas_GATEKEEPER_CLIENT")

GATEKEEPER_URL = os.getenv("GATEKEEPER_URL", "http://gravitas_gatekeeper:8001")

class GatekeeperClient:
    """
    Client for interacting with the Gatekeeper Microservice.
    Includes Circuit Breaker pattern with fallback to local logic.
    """
    def __init__(self):
        self.circuit_open = False
        # We could implement a real circuit breaker, but for now simple exception handling is enough
        
    async def validate_request(self, token: str, action: str, resource: str, metadata: Dict = None) -> Dict:
        """
        Validates a request via Gatekeeper.
        Falls back to local validation if Gatekeeper is unreachable.
        """
        if not self.circuit_open:
            try:
                async with httpx.AsyncClient(timeout=0.5) as client: # strict timeout
                    payload = {
                        "action": action,
                        "resource": resource,
                        "metadata": metadata
                    }
                    headers = {"Authorization": f"Bearer {token}"}
                    
                    response = await client.post(f"{GATEKEEPER_URL}/validate", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code in [401, 403]:
                        # Gatekeeper explicitly denied it. Respect that.
                        # We return the error detail to be raised by caller
                        return {"allowed": False, "error_code": response.status_code, "detail": response.json().get("detail")}
                    else:
                        logger.warning(f"Gatekeeper returned unexpected status {response.status_code}. Falling back.")
                        # server error, fall back
                        
            except httpx.RequestError as e:
                logger.error(f"Gatekeeper unreachable: {e}. Falling back to local validation.")
                # Fallback
            except Exception as e:
                logger.error(f"Gatekeeper client error: {e}. Falling back.")

        # --- FALLBACK LOGIC (Local Auth/Policy) ---
        return await self._validate_local(token, action, resource, metadata)

    async def _validate_local(self, token: str, action: str, resource: str, metadata: Dict) -> Dict:
        """Local validation mirroring Gatekeeper logic."""
        logger.info(f"⚠️ Using LOCAL validation fallback for {resource}")
        
        # 1. Auth
        claims = decode_access_token(token)
        if not claims:
             return {"allowed": False, "error_code": 401, "detail": "Invalid or expired token (Local)"}
             
        ghost_id = claims.get("sub")
        groups = claims.get("groups", [])
        
        # 2. Policy
        allowed = policy_engine.check_permission(
            ghost_id=ghost_id,
            action=action,
            resource=resource
        )
        
        # 3. Audit (Local)
        audit_result = "ALLOWED" if allowed else "DENIED"
        audit_reason = None if allowed else "Policy denied"
        
        event = AuditEvent(
            action=action,
            resource=resource,
            ghost_id=ghost_id,
            shell_id=metadata.get("shell_id") if metadata else None,
            result=audit_result,
            reason=audit_reason,
            metadata=metadata
        )
        await audit_logger.log_event(event)
        
        if not allowed:
             return {"allowed": False, "error_code": 403, "detail": "Access denied by policy (Local)"}
             
        return {
            "allowed": True,
            "ghost_id": ghost_id,
            "groups": groups,
            "audit_id": "local",
            "reason": "Authorized (Local)"
        }

gatekeeper_client = GatekeeperClient()
