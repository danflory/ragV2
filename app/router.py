import logging
import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx
from pydantic import BaseModel
import asyncio
import json
import subprocess
import os

from .container import container
from .config import config
from .database import db

logger = logging.getLogger("Gravitas_LEGACY_ROUTER")

router = APIRouter()

# --- DEPRECATION NOTICE ---
# This router is being decommissioned in Phase 7.
# All clients should migrate to the Supervisor on Port 8000.

@router.post("/chat")
async def chat_endpoint():
    raise HTTPException(
        status_code=410, 
        detail="The /chat endpoint is DEPRECATED. Please use the Supervisor at http://localhost:8000/v1/chat/completions"
    )

@router.get("/health/detailed")
async def get_detailed_health():
    """
    Checks connectivity for all microservices and GPU stats.
    Legacy fallback for dashboard.
    """
    health = {
        "api": "online",
        "postgres": "online" if db.is_ready() else "offline",
        "qdrant": "offline",
        "minio": "offline",
        "ollama": "offline",
        "ollama_embed": "offline",
        "gpu": {"used": 0, "total": 0, "percentage": 0}
    }
    
    # Check Ollama
    if await container.l1_driver.check_health():
        health["ollama"] = "online"
        
    # Check Ollama Embed
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(config.L1_EMBED_URL)
            if resp.status_code == 200:
                health["ollama_embed"] = "online"
    except:
        pass

    # Check Qdrant
    if container.memory and await container.memory.check_health():
        health["qdrant"] = "online"
        
    # Check MinIO
    if container.storage and await container.storage.check_health():
        health["minio"] = "online"

    # Check GPU (NVIDIA)
    try:
        res = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], encoding="utf-8")
        lines = res.strip().split("\n")
        if lines:
            used, total = map(int, lines[0].split(","))
            health["gpu"] = {
                "used": used,
                "total": total,
                "percentage": round((used / total) * 100, 1) if total > 0 else 0
            }
    except Exception as e:
        logger.warning(f"Failed to fetch GPU stats: {e}")
        
    return {"status": "success", "health": health, "current_mode": container.current_mode}

@router.get("/health/stream")
async def health_stream(request: Request):
    """
    SSE stream fallback for dashboard.
    """
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            health_data = await get_detailed_health()
            yield f"event: update\ndata: {json.dumps(health_data)}\n\n"
            await asyncio.sleep(5) # Reduced frequency for legacy endpoint

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "router": "legacy"}