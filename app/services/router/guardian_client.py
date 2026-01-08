import httpx
import logging
import os
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger("Gravitas_ROUTER_GUARDIAN_CLIENT")

@dataclass
class SessionPermission:
    allowed: bool
    reason: Optional[str] = None

class AgentNotCertifiedError(Exception):
    pass

class GuardianClient:
    """
    Client for interacting with the Guardian Microservice.
    No local fallback in Router service.
    """
    
    def __init__(self, guardian_url: Optional[str] = None, fallback_to_local: bool = False, timeout: float = 5.0):
        self.guardian_url = guardian_url or os.getenv("GUARDIAN_URL", "http://gravitas_guardian:8003")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)
        if fallback_to_local:
            logger.warning("Local fallback not supported in Router service. Ignoring.")
    
    async def notify_session_start(self, agent: str, session_id: str, metadata: dict) -> SessionPermission:
        try:
            resp = await self.client.post(
                f"{self.guardian_url}/session/start",
                json={
                    "agent": agent,
                    "session_id": session_id,
                    "metadata": metadata
                }
            )
            resp.raise_for_status()
            data = resp.json()
            return SessionPermission(allowed=data["allowed"], reason=data.get("reason"))
        except Exception as e:
            logger.error(f"Guardian service check failed: {e}")
            # Fail closed for security? Or open for resilience?
            # Phase 1 verification said Guardian should be non-blocking for failures if possible, 
            # but strict for denials.
            # If service is down, we can't verify cert.
            raise AgentNotCertifiedError("Guardian service unavailable")

    async def notify_session_end(self, session_id: str, output_file: Path):
        try:
            await self.client.post(
                f"{self.guardian_url}/session/end",
                json={"session_id": session_id, "output_file": str(output_file)}
            )
        except Exception as e:
            logger.warning(f"Failed to notify session end: {e}")

    async def validate_certificate(self, agent: str) -> bool:
        try:
            resp = await self.client.post(
                f"{self.guardian_url}/validate",
                json={"agent": agent}
            )
            resp.raise_for_status()
            return True
        except Exception:
            return False

    async def close(self):
        await self.client.aclose()
