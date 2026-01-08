import logging
import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from contextlib import asynccontextmanager

from app.services.gatekeeper.auth import decode_access_token
from app.services.gatekeeper.policy import policy_engine
from app.services.gatekeeper.audit import audit_logger, AuditEvent
from app.services.gatekeeper.database import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Gravitas_GATEKEEPER_SERVICE")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🛡️ Gatekeeper Service starting up...")
    try:
        await db.connect()
        await db.init_schema()
        logger.info("✅ Database connected.")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        # We might want to exit here if DB is critical, but for now log it.
    
    yield
    
    # Shutdown
    await db.disconnect()
    logger.info("🛑 Gatekeeper Service shutting down.")

app = FastAPI(
    title="Gravitas Gatekeeper Service",
    description="Security microservice for Authentication, Authorization, and Audit Logging.",
    version="1.0.0",
    lifespan=lifespan
)

class ValidateRequest(BaseModel):
    # Metadata about the request for policy checking
    action: str = "inference" # default to inference
    resource: str # e.g. model name "gemma2:27b"
    metadata: Optional[Dict] = None

class ValidateResponse(BaseModel):
    allowed: bool
    ghost_id: Optional[str] = None
    groups: List[str] = []
    audit_id: Optional[str] = None # Placeholder if we return ID
    reason: Optional[str] = None

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "gatekeeper",
        "database": db.is_ready()
    }

@app.post("/validate", response_model=ValidateResponse)
async def validate_request(
    request: ValidateRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Validates a request:
    1. Checks JWT (Authentication)
    2. Checks Policy (Authorization)
    3. Logs Audit Event (Audit)
    """
    
    # 1. Authentication
    if os.getenv("AUTH_DISABLED", "false").lower() == "true":
        claims = {"sub": "Supervisor_Managed_Agent", "groups": ["admin"]}
    else:
        if not authorization:
            # Audit the failure?
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        
        token = authorization.replace("Bearer ", "")
        claims = decode_access_token(token)
        
        if not claims:
            # Audit failure?
            logger.warning("Invalid token presented")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    ghost_id = claims.get("sub")
    groups = claims.get("groups", [])
    
    # 2. Authorization
    allowed = policy_engine.check_permission(
        ghost_id=ghost_id,
        action=request.action,
        resource=request.resource
    )
    
    # 3. Audit Logging
    audit_result = "ALLOWED" if allowed else "DENIED"
    audit_reason = None if allowed else "Policy denied"
    
    event = AuditEvent(
        action=request.action,
        resource=request.resource,
        ghost_id=ghost_id,
        shell_id=request.metadata.get("shell_id") if request.metadata else None,
        result=audit_result,
        reason=audit_reason,
        metadata=request.metadata
    )
    
    # Fire and forget audit log (async)
    # Note: treating this as "best effort". 
    # Ideally use background task to not block response if DB is slow
    await audit_logger.log_event(event)

    if not allowed:
        raise HTTPException(status_code=403, detail="Access denied by policy")

    return {
        "allowed": True,
        "ghost_id": ghost_id,
        "groups": groups,
        "audit_id": "pending", # We don't wait for ID
        "reason": "Authorized"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
