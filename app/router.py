import logging
from fastapi import APIRouter
from pydantic import BaseModel
import GPUtil

from .config import config
from .container import container
from .reflex import execute_git_sync

logger = logging.getLogger("AGY_Router")

class ChatRequest(BaseModel):
    message: str

router = APIRouter()

def check_vram_headroom(threshold_gb=2.0) -> bool:
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            if "TITAN RTX" in gpu.name.upper():
                return (gpu.memoryFree / 1024) > threshold_gb
        return True
    except:
        return True

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. Hardware Guard (Fixed Variable Name)
    # We check config.L1_MODEL instead of config.MODEL
    if config.L1_MODEL == "deepseek-coder-v2:16b" and not check_vram_headroom(config.VRAM_THRESHOLD_GB):
        return {"response": "ESCALATE TO L2 (VRAM Limit)"}

    # 2. Get L1 Response
    response_text = await container.l1_driver.generate(request.message)
    
    # 3. === REFLEX INTERCEPTOR ===
    if response_text == "<<GIT_SYNC>>":
        action_log = execute_git_sync()
        return {"response": action_log}
    
    # 4. Handle Escalation
    if response_text == "ESCALATE TO L2":
        return {"response": "ESCALATE TO L2"}
    
    return {"response": response_text}