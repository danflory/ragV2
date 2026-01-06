from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import asyncio
import logging
from typing import Dict, Any

# Relative imports from copied logic
from services.dispatcher.router import DispatcherRouter, UserQuery, TelemetryState, TargetModel
from services.scheduler.queue import RequestQueue
from services.scheduler.lock import ModelLock
from clients.deepinfra import DeepInfraClient
from clients.gemini import GeminiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("supervisor")

app = FastAPI(title="Gravitas Supervisor")

# Global Components
router = DispatcherRouter()
queue = RequestQueue()
model_lock = ModelLock()

# Clients
deepinfra = DeepInfraClient()
gemini = GeminiClient()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://Gravitas_ollama:11434/v1/chat/completions")

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    OpenAI-compatible chat completions endpoint with intelligent routing and queuing.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Extract query and metadata
    messages = body.get("messages", [])
    user_text = messages[-1].get("content", "") if messages else ""
    
    # Mock complexity or extract from body if available
    complexity = body.get("complexity", 5)
    
    # Mock telemetry (in real scenario, this would come from a telemetry service)
    # We'll assume normal state for now
    telemetry = TelemetryState(
        vram_usage_percent=40.0,
        system_load_percent=10.0,
        avg_latency=0.5
    )

    # 1. Route the request
    query = UserQuery(text=user_text, code_complexity=complexity)
    target = router.route(query, telemetry)
    logger.info(f"Routing query to {target.value} (Complexity: {complexity})")

    # 2. Handle Routing
    if target == TargetModel.L3:
        # Use Gemini
        res = await gemini.generate_content("gemini-1.5-flash", [{"parts": [{"text": user_text}]}])
        if "error" in res:
             return JSONResponse(res, status_code=500)
        # Convert Gemini response to OpenAI format
        content = res.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error")
        return {"choices": [{"message": {"content": content}}]}

    elif target == TargetModel.L2:
        # Use DeepInfra
        res = await deepinfra.chat_completion(body.get("model", "meta-llama/Meta-Llama-3-70B-Instruct"), messages)
        return JSONResponse(res)

    else:
        # L1: Local Ollama (With Queuing)
        # 3. Enqueue for Local processing
        await queue.enqueue(body, priority=5)
        logger.info(f"Enqueued L1 request. Queue size: {queue.qsize()}")
        
        # 4. Dequeue and Process (Simple serial processing for now)
        # In a real system, a background worker would do this.
        # Here we'll just process it immediately to fulfill the request.
        queued_body = await queue.dequeue()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(OLLAMA_URL, json=queued_body, timeout=120.0)
                return JSONResponse(content=response.json(), status_code=response.status_code)
            except Exception as e:
                logger.error(f"L1 Error: {e}")
                return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "queue_size": queue.qsize(),
        "hot_model": model_lock.current_model
    }
