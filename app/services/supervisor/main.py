import uvicorn
import os
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import db
from app.services.supervisor.router import router as supervisor_router

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
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
    
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

# Include the supervisor routes
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
