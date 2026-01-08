import uvicorn
import os
import logging
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Depends
from contextlib import asynccontextmanager
from app.services.supervisor.database import db
from app.services.supervisor.router import router as supervisor_router, engine
# from app.services.security.auth import decode_access_token # Removed
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
        await db.init_schema()
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

# Public Health Endpoint (No Auth)
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "queue_size": engine.queue.qsize(),
        "active_workers": engine.active_workers,
        "mode": "standalone"
    }

# Include the supervisor routes (Auth handled internally by router via Gatekeeper)
app.include_router(supervisor_router)

@app.get("/")
async def root():
    return {
        "service": "Gravitas Supervisor",
        "status": "online",
        "endpoints": ["/v1/chat/completions", "/health"]
    }

if __name__ == "__main__":
    uvicorn.run("app.services.supervisor.main:app", host="0.0.0.0", port=8000, reload=True)
