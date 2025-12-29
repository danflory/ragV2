from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .router import router as chat_router
from .config import config
from .L1_local import l1_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Verify L1 Model is pulled and ready
    print(f"🚀 AGY Starting up... Target L1: {config.MODEL}")
    is_ready = await l1_engine.check_model_exists()
    if not is_ready:
        print("⚠️ WARNING: L1 Model not found. L1 calls will auto-escalate to L2.")
    yield
    # SHUTDOWN: Logic for closing DB connections can go here
    print("🛑 AGY Shutting down...")

app = FastAPI(title="Google AntiGravity API", version="0.6", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {
        "status": "online",
        "active_L1_model": config.MODEL,
        "mode": "3L-Hybrid"
    }