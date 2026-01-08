import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.router.api import router
from app.services.router.database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gravitas_ROUTER_MAIN")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Gravitas Router Service Starting...")
    await db.connect()
    await db.init_schema()
    yield
    # Shutdown
    await db.disconnect()
    logger.info("Gravitas Router Service Stopping...")

app = FastAPI(title="Gravitas Router", lifespan=lifespan)

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
