from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .router import router as chat_router
from .config import config
from .container import container

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Initialize Postgres Connection
    from .database import db
    await db.connect()
    
    # STARTUP: Verify L1 Model is pulled and ready
    print(f"🚀 AGY Starting up... Target L1: {config.L1_MODEL}")
    
    # Check health and pull model if needed
    is_ready = await container.l1_driver.check_health()
    if is_ready:
        await container.l1_driver.ensure_model()
    else:
        print("⚠️ WARNING: L1 Backend (Ollama) not responding. L1 calls will fail or escalate.")
    yield
    # SHUTDOWN
    await db.disconnect()
    print("🛑 AGY Shutting down...")

app = FastAPI(
    title="AntiGravity RAG Server",
    version="1.0.0",
    lifespan=lifespan
)

# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all. Change this for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {
        "status": "online",
        "active_L1_model": config.L1_MODEL,
        "mode": "3L-Hybrid"
    }