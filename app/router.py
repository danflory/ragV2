import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import GPUtil
from .config import config
# OLD: from .L1_local import l1_engine
# NEW: Import the container instead
from .container import container

logger = logging.getLogger("AGY_Router")

class ChatRequest(BaseModel):
    message: str
    model_override: str = None

router = APIRouter()

def check_vram_headroom(threshold_gb=2.0) -> bool:
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            if "TITAN RTX" in gpu.name.upper():
                free_vram = gpu.memoryFree / 1024
                logger.info(f"🎨 Titan RTX VRAM Free: {free_vram:.2f}GB")
                return free_vram > threshold_gb
        return True
    except Exception as e:
        logger.warning(f"⚠️ VRAM Check failed: {e}")
        return True

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. Hardware Guard
    if config.MODEL == "deepseek-coder-v2:16b":
        if not check_vram_headroom(config.VRAM_THRESHOLD_GB):
            logger.warning("⛔ VRAM Constrained. Bypassing L1.")
            return {"response": "ESCALATE TO L2 (VRAM Limit)"}

    # 2. Try Local L1 Inference
    # NEW: Use the container to get the driver
    # Note: We use the standardized .generate() method now!
    response = await container.l1_driver.generate(request.message)
    
    # 3. Handle Escalation
    if response == "ESCALATE TO L2":
        return {"response": "ESCALATE TO L2"}
    
    return {"response": response}