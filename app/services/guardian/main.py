"""
Gravitas Guardian Service

Manages agent certification and session tracking.
Ensures only certified agents can execute tasks.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging
import os

from app.services.guardian.core import (
    SupervisorGuardian,
    AgentNotCertifiedError,
    CertificationExpiredError
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gravitas_GUARDIAN_SERVICE")

app = FastAPI(title="Gravitas Guardian Service", version="1.0.0")

# Initialize Guardian with certificates directory
certificates_dir = os.getenv("CERTIFICATES_DIR", "app/.certificates")
guardian = SupervisorGuardian(certificates_dir=certificates_dir)

logger.info(f"🛡️  Guardian Service initialized with {len(guardian.certified_agents)} certificates")


# --- Request/Response Models ---

class SessionStartRequest(BaseModel):
    agent: str
    session_id: str
    metadata: dict


class SessionEndRequest(BaseModel):
    session_id: str
    output_file: str


class ValidateCertificateRequest(BaseModel):
    agent: str


# --- API Endpoints ---

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "guardian",
        "certificates_loaded": len(guardian.certified_agents),
        "active_sessions": len(guardian.active_sessions),
        "completed_sessions": len(guardian.completed_sessions)
    }


@app.post("/validate")
async def validate_certificate(req: ValidateCertificateRequest):
    """
    Validate if an agent has a valid, non-expired certificate.
    """
    if req.agent not in guardian.certified_agents:
        logger.warning(f"Certificate validation failed: {req.agent} not certified")
        raise HTTPException(
            status_code=403,
            detail=f"Agent '{req.agent}' lacks a valid certificate"
        )
    
    cert = guardian.certified_agents[req.agent]
    now = datetime.now(cert.expires_at.tzinfo) if cert.expires_at.tzinfo else datetime.now()
    
    if now > cert.expires_at:
        logger.warning(f"Certificate validation failed: {req.agent} expired at {cert.expires_at}")
        raise HTTPException(
            status_code=403,
            detail=f"Certificate for '{req.agent}' expired on {cert.expires_at.isoformat()}"
        )
    
    logger.info(f"✅ Certificate valid for {req.agent} (expires: {cert.expires_at.isoformat()})")
    return {
        "valid": True,
        "agent": req.agent,
        "expires_at": cert.expires_at.isoformat(),
        "issued_at": cert.issued_at.isoformat()
    }


@app.post("/session/start")
async def session_start(req: SessionStartRequest):
    """
    Notify Guardian of a session start.
    Validates certificate and tracks active session.
    """
    try:
        permission = await guardian.notify_session_start(
            agent=req.agent,
            session_id=req.session_id,
            metadata=req.metadata
        )
        
        logger.info(f"📝 Session started: {req.session_id} for agent {req.agent}")
        return {
            "allowed": permission.allowed,
            "reason": permission.reason
        }
        
    except AgentNotCertifiedError as e:
        logger.error(f"Session start denied: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    
    except CertificationExpiredError as e:
        logger.error(f"Session start denied: {e}")
        raise HTTPException(status_code=403, detail=str(e))


@app.post("/session/end")
async def session_end(req: SessionEndRequest):
    """
    Notify Guardian of session completion.
    Updates session tracking and statistics.
    """
    from pathlib import Path
    
    await guardian.notify_session_end(
        session_id=req.session_id,
        output_file=Path(req.output_file)
    )
    
    logger.info(f"✅ Session completed: {req.session_id}")
    return {"status": "session_closed", "session_id": req.session_id}


@app.get("/stats")
async def get_stats(agent: Optional[str] = None):
    """
    Get session statistics for monitoring.
    Optionally filter by specific agent.
    """
    stats = guardian.get_session_stats(agent=agent)
    return {
        "stats": stats,
        "total_agents": len(stats),
        "query_agent": agent
    }


@app.get("/certificates")
async def list_certificates():
    """
    List all loaded certificates.
    """
    certs = []
    for agent_name, cert in guardian.certified_agents.items():
        now = datetime.now(cert.expires_at.tzinfo) if cert.expires_at.tzinfo else datetime.now()
        certs.append({
            "agent": agent_name,
            "issued_at": cert.issued_at.isoformat(),
            "expires_at": cert.expires_at.isoformat(),
            "version": cert.version,
            "is_expired": now > cert.expires_at
        })
    
    return {
        "certificates": certs,
        "total": len(certs)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
