import uvicorn
import os
import logging
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Depends
from contextlib import asynccontextmanager
from app.database import db
from app.services.supervisor.router import router as supervisor_router, engine
from app.services.security.auth import decode_access_token
from app.services.security.badges import badge_system

# ... (rest of imports)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Gravitas_SUPERVISOR_SERVICE")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Database
    logger.info("🚀 Supervisor Service starting up...")
    try:
        await db.connect()
        logger.info("✅ Database connected.")
        
        # Initialize badge cache
        await badge_system.init_cache()
        logger.info("✅ Badge registry initialized.")
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
    
    yield
    
    # Shutdown: Disconnect
    await db.disconnect()
    logger.info("🛑 Supervisor Service shutting down.")

app = FastAPI(
    title="Gravitas Supervisor Service",
    description="Intelligent routing and agent governance gateway.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Security Middleware ---

async def require_auth(authorization: Optional[str] = Header(None)):
    """FastAPI dependency to enforce JWT authentication."""
    if os.getenv("AUTH_DISABLED", "false").lower() == "true":
        return {"sub": "anonymous", "groups": ["admin"]}
        
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    return payload

# Public Health Endpoint (No Auth)
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "queue_size": engine.queue.qsize(),
        "active_workers": engine.active_workers,
        "mode": "standalone"
    }

# Include the supervisor routes with authentication
app.include_router(supervisor_router, dependencies=[Depends(require_auth)])

@app.get("/")
async def root():
    return {
        "service": "Gravitas Supervisor",
        "status": "online",
        "endpoints": ["/v1/chat/completions", "/health"]
    }

if __name__ == "__main__":
    uvicorn.run("app.services.supervisor.main:app", host="0.0.0.0", port=8000, reload=True)
