import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class AgentNotCertifiedError(Exception):
    """Raised when an agent is not certified."""
    pass

class CertificationExpiredError(Exception):
    """Raised when an agent's certification has expired."""
    pass

@dataclass
class Certificate:
    agent_name: str
    issued_at: datetime
    expires_at: datetime
    signature: str
    version: str = "1.0"

    @classmethod
    def from_dict(cls, data: dict) -> 'Certificate':
        return cls(
            agent_name=data["agent_name"],
            issued_at=datetime.fromisoformat(data["issued_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]),
            signature=data["signature"],
            version=data.get("version", "1.0")
        )

@dataclass
class SessionPermission:
    allowed: bool
    reason: Optional[str] = None

class SupervisorGuardian:
    """
    Enforces that only certified agents can execute.
    """

    def __init__(self, certificates_dir: str = "app/.certificates"):
        self.certificates_dir = Path(certificates_dir)
        self.certified_agents: Dict[str, Certificate] = self._load_certificates()
        self.active_sessions: Dict[str, dict] = {}  # {session_id: session_metadata}
        self.completed_sessions: List[dict] = []
        
        logger.info(f"SupervisorGuardian initialized with {len(self.certified_agents)} certificates.")

    def _load_certificates(self) -> Dict[str, Certificate]:
        """
        Reads all JSON files in the certificates directory.
        """
        certs = {}
        if not self.certificates_dir.exists():
            logger.warning(f"Certificates directory {self.certificates_dir} does not exist.")
            return certs

        for cert_file in self.certificates_dir.glob("*.json"):
            try:
                with open(cert_file, "r") as f:
                    data = json.load(f)
                    cert = Certificate.from_dict(data)
                    certs[cert.agent_name] = cert
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Failed to load certificate from {cert_file}: {e}")
        
        return certs

    async def notify_session_start(
        self, 
        agent: str, 
        session_id: str,
        metadata: dict
    ) -> SessionPermission:
        """
        Called by agent wrapper before task execution.
        """
        if agent not in self.certified_agents:
            logger.error(f"Agent {agent} is not certified.")
            raise AgentNotCertifiedError(f"Agent '{agent}' lacks a valid certificate.")

        cert = self.certified_agents[agent]
        now = datetime.now()

        if now > cert.expires_at:
            logger.error(f"Certificate for {agent} expired at {cert.expires_at}.")
            raise CertificationExpiredError(f"Certificate for '{agent}' expired on {cert.expires_at}.")

        # Check for existing session conflicts (optional reinforcement)
        if session_id in self.active_sessions:
            return SessionPermission(allowed=False, reason=f"Session {session_id} is already active.")

        self.active_sessions[session_id] = {
            "agent": agent,
            "start_time": now,
            "metadata": metadata,
            "status": "active"
        }

        return SessionPermission(allowed=True)

    async def notify_session_end(
        self, 
        session_id: str,
        output_file: Path
    ):
        """
        Called by agent wrapper after pipe.finalize().
        """
        if session_id not in self.active_sessions:
            logger.warning(f"Received notify_session_end for unknown session {session_id}.")
            return

        session = self.active_sessions.pop(session_id)
        end_time = datetime.now()
        duration = (end_time - session["start_time"]).total_seconds()
        
        session.update({
            "end_time": end_time,
            "duration": round(duration, 2),
            "output_file": str(output_file),
            "status": "completed"
        })
        
        self.completed_sessions.append(session)
        logger.info(f"Session {session_id} completed. Duration: {session['duration']}s")

    def get_session_stats(self, agent: Optional[str] = None) -> dict:
        """
        Returns session statistics for monitoring.
        """
        stats = {}
        
        agents_to_query = [agent] if agent else self.certified_agents.keys()
        
        for agent_name in agents_to_query:
            active_count = sum(1 for s in self.active_sessions.values() if s["agent"] == agent_name)
            completed_for_agent = [s for s in self.completed_sessions if s["agent"] == agent_name]
            
            avg_duration = 0
            if completed_for_agent:
                avg_duration = round(sum(s["duration"] for s in completed_for_agent) / len(completed_for_agent), 2)
            
            cert = self.certified_agents.get(agent_name)
            cert_expiry = cert.expires_at.isoformat() if cert else None
            
            stats[agent_name] = {
                "active_sessions": active_count,
                "completed_total": len(completed_for_agent),
                "avg_duration": avg_duration,
                "certification_expires": cert_expiry
            }
            
        return stats
