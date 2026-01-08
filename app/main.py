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
    print(f"🚀 Gravitas Starting up... Target L1: {config.L1_MODEL}")
    
    # Check health and pull model if needed
    is_ready = await container.l1_driver.check_health()
    if is_ready:
        await container.l1_driver.ensure_model()
    else:
        print("⚠️ WARNING: L1 Backend (Ollama) not responding. L1 calls will fail or escalate.")
    yield
    # SHUTDOWN
    await db.disconnect()
    print("🛑 Gravitas Shutting down...")

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Gravitas Grounded Research",
    description="Dual-GPU Production-Grade Hybrid RAG Architecture",
    version="4.2.0",
    lifespan=lifespan
)

# MOUNT DASHBOARD (STATIC FILES)
dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")

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
        "active_L1_model": container.l1_driver.model_name,
        "mode": container.current_mode
    }

@app.get("/v1/registry/models")
async def get_models(tier: str = None, provider: str = None):
    """
    Get all available models from the registry.
    Optional filters: tier (L1/L2/L3), provider (ollama/google/anthropic/deepinfra)
    """
    from .services.registry.shell_registry import ShellRegistry, ModelTier
    
    # Get all models
    all_models = ShellRegistry.get_all_models()
    
    # Apply filters
    filtered_models = {}
    for name, spec in all_models.items():
        # Tier filter
        if tier and spec.tier.value != tier:
            continue
        # Provider filter  
        if provider and spec.provider != provider:
            continue
        
        # Convert to dict for JSON response
        filtered_models[name] = {
            "name": spec.name,
            "tier": spec.tier.value,
            "provider": spec.provider,
            "cost_per_1k_tokens": spec.cost_per_1k_tokens,
            "context_window": spec.context_window,
            "avg_latency_ms": spec.avg_latency_ms,
            "capabilities": [cap.value for cap in spec.capabilities],
            "specialty": spec.specialty,
            "vram_required_gb": spec.vram_required_gb
        }
    
    return {
        "models": filtered_models,
        "count": len(filtered_models)
    }

if os.path.exists(dashboard_path):
    from fastapi.responses import FileResponse
    
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(dashboard_path, "index.html"))

    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")