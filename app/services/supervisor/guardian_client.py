"""
Guardian Client for Supervisor

HTTP client wrapper for calling the Guardian service.
Includes fallback to local Guardian for resilience during Phase 1.
"""
import httpx
import logging
import os
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

from app.services.supervisor.guardian import (
    SupervisorGuardian,
    AgentNotCertifiedError,
    CertificationExpiredError,
    SessionPermission
)

logger = logging.getLogger("Gravitas_SUPERVISOR_GUARDIAN_CLIENT")


class GuardianClient:
    """
    HTTP client for Guardian service with local fallback capability.
    
    During Phase 1, fallback to local Guardian is enabled for safety.
    In Phase 1.3, fallback will be disabled and Guardian service becomes
    the single source of truth.
    """
    
    def __init__(
        self,
        guardian_url: Optional[str] = None,
        fallback_to_local: bool = True,
        timeout: float = 5.0
    ):
        self.guardian_url = guardian_url or os.getenv(
            "GUARDIAN_URL",
            "http://gravitas_guardian:8003"
        )
        self.fallback_to_local = fallback_to_local
        self.timeout = timeout
        
        # Initialize local Guardian if fallback enabled
        self.local_guardian = None
        if self.fallback_to_local:
            try:
                self.local_guardian = SupervisorGuardian()
                logger.info("Local Guardian fallback initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize local Guardian fallback: {e}")
        
        self.client = httpx.AsyncClient(timeout=self.timeout)
        logger.info(f"Guardian client initialized (service: {self.guardian_url}, fallback: {fallback_to_local})")
    
    async def notify_session_start(
        self,
        agent: str,
        session_id: str,
        metadata: dict
    ) -> SessionPermission:
        """
        Notify Guardian of session start.
        Falls back to local Guardian if service unavailable.
        """
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
            logger.warning(f"Guardian service error during session_start: {e}")
            
            if self.local_guardian:
                logger.info("⚠️  Falling back to local Guardian")
                return await self.local_guardian.notify_session_start(agent, session_id, metadata)
            
            # No fallback available
            raise AgentNotCertifiedError(
                f"Guardian service unavailable and no fallback configured: {e}"
            )
    
    async def notify_session_end(
        self,
        session_id: str,
        output_file: Path
    ):
        """
        Notify Guardian of session completion.
        Falls back to local Guardian if service unavailable.
        """
        try:
            resp = await self.client.post(
                f"{self.guardian_url}/session/end",
                json={
                    "session_id": session_id,
                    "output_file": str(output_file)
                }
            )
            resp.raise_for_status()
            
        except Exception as e:
            logger.warning(f"Guardian service error during session_end: {e}")
            
            if self.local_guardian:
                logger.info("⚠️  Falling back to local Guardian")
                await self.local_guardian.notify_session_end(session_id, output_file)
            else:
                # Log but don't raise - session end is best-effort
                logger.error(f"Failed to notify Guardian of session end: {e}")
    
    async def validate_certificate(self, agent: str) -> bool:
        """
        Quick certificate validation check.
        Returns True if valid, False otherwise.
        """
        try:
            resp = await self.client.post(
                f"{self.guardian_url}/validate",
                json={"agent": agent}
            )
            resp.raise_for_status()
            return True
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                return False
            raise
            
        except Exception as e:
            logger.warning(f"Guardian service error during validation: {e}")
            
            if self.local_guardian:
                logger.info("⚠️  Falling back to local Guardian")
                return agent in self.local_guardian.certified_agents
            
            return False
    
    async def get_session_stats(self, agent: Optional[str] = None) -> dict:
        """
        Get session statistics from Guardian.
        Falls back to local Guardian if service unavailable.
        """
        try:
            params = {"agent": agent} if agent else {}
            resp = await self.client.get(
                f"{self.guardian_url}/stats",
                params=params
            )
            resp.raise_for_status()
            return resp.json()
            
        except Exception as e:
            logger.warning(f"Guardian service error during stats retrieval: {e}")
            
            if self.local_guardian:
                logger.info("⚠️  Falling back to local Guardian")
                return self.local_guardian.get_session_stats(agent=agent)
            
            return {"error": str(e)}
    
    async def close(self):
        """Close HTTP client connection"""
        await self.client.aclose()
