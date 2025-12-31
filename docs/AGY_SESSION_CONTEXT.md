
# AntiGravity RAG - Session Context
**Generated:** 2025-12-30 21:01:40
**L2 Provider:** DeepInfra (DeepSeek/Qwen)
**App State:** Dockerization / Security Hardening

## 1. IMMEDIATE TODO LIST
* [CRITICAL] **Secret Hygiene:** Scan codebase for hardcoded keys and move to `.env`.
* [HIGH] **Docker:** Finalize `docker-compose.yml` for GPU passthrough.
* [MED] **L2 Driver:** Verify `DeepInfra` integration in `L2_network.py`.
* [MED] **Gatekeeper:** Implement pre-commit hooks for safety.

## 2. RECENT CHANGES (The Delta)
* Split Spec into Hardware (Static) and App (Dynamic).
* Deprecated OpenRouter.
* Enforced 32GB RAM limit in documentation.

---
## 3. PHYSICAL FILE MAP
```text
rag_local/
    test_l1.py
    t3.txt
    t2.txt
    .gitignore
    testResults.txt
    l1_review_dan.txt
    test.txt
    check_vram.py
    rag_memory.db
    threshold_gb
    docker-compose.yml
    memory_check.txt
    requirements.txt
    .env
    .dockerignore
    Dockerfile
    memory.db
    chat_history.db
    testResults1.txt
    who_am_i.txt
    rag_local.code-workspace
    log_conf.yaml
    test_memory.txt
        docs/
            AGY_Architecture_Spec.md
            AGY_HARDWARE_CTX.md
            AGY_SYSTEM_SPEC.md
            DansRig.md
            AGY_SESSION_CONTEXT.md
            dan's updated rig
            initialAgySetupChat
            AntiGravityDevPlan.md
        rag_local/
        data/
            knowledge.json
            models/
            chroma_data/
        app/
            config.py
            interfaces.py
            main.py
            L1_local.py
            L2_network.py
            database.py
            system_log.py
            router.py
            reflex.py
            container.py
            memory.py
            app/
                ingestor.py
        tests/
            test_L3_google.py
            test_L2_config.py
            test_ioc_refactor.py
            test_3L_pipeline.py
            test_L1_fail.py
            test_ioc_baseline.py
            test_reflex.py
            test_current_stack.py
        scripts/
            log_entry.py
            verify_chat.py
            load_knowledge.py
            agy_writer.py
            audit_agy.sh
            warmup.py
            debug_import.py
            test_retrieval.py
            router_refactored.py
            generate_session_context.py
            reset_agy.sh
            check_models.py
            debug_network.py
            titan_stress.py
```

---
## 4. CRITICAL FILE CONTENTS

### File: `app/main.py`
```python
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
```

### File: `app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # === GLOBAL IDENTITY ===
    USER_NAME: str = "Dan"
    PORT: int = 5050
    
    # === LAYER 1 (Local - Titan RTX) ===
    L1_URL: str = "http://127.0.0.1:11434"
    L1_MODEL: str = "codellama:7b"
    VRAM_THRESHOLD_GB: float = 2.0
    
    # === LAYER 2 (Cloud - Reasoning/Coding) ===
    L2_KEY: str | None = None
    L2_URL: str = "https://api.deepinfra.com/v1/openai/chat/completions"
    L2_MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"

    # === LAYER 3 (Agents - Google Gemini 3) ===
    L3_KEY: str | None = None
    # Default to Gemini 3 Pro Preview
    L3_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
    L3_MODEL: str = "gemini-3-pro-preview"

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Settings()
```

### File: `app/L2_network.py`
```python
import httpx
import logging
from .interfaces import LLMDriver
from .config import Settings

logger = logging.getLogger("AGY_CLOUD")

class UniversalCloudDriver(LLMDriver):
    """
    The Universal Driver.
    Handles both OpenAI-compatible APIs (DeepInfra/DeepSeek) AND Google Gemini.
    Auto-detects format based on the URL.
    """
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model
        
    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return f"[System Error: Missing API Key for {self.model_name}]"

        # 1. Detect Provider
        is_google = "googleapis.com" in self.base_url

        # 2. Build Headers & Payload accordingly
        if is_google:
            # === GOOGLE GEMINI MODE ===
            url = f"{self.base_url}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7
                }
            }
        else:
            # === OPENAI / DEEPINFRA / DEEPSEEK MODE ===
            url = self.base_url
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a precise and helpful AI."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6
            }

        # 3. Fire the Request
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Cloud Error ({self.model_name}): {response.text}")
                    return f"[API Error {response.status_code}: {response.text}]"

                data = response.json()
                
                # 4. Parse Response (Different paths for Google vs OpenAI)
                if is_google:
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    return data['choices'][0]['message']['content']

        except Exception as e:
            logger.error(f"Connection Exception: {e}")
            return f"[Connection Error: {str(e)}]"

    async def check_health(self) -> bool:
        return bool(self.api_key)
```

### File: `app/router.py`
```python
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
```

### File: `Dockerfile`
```python
# 1. Use the same lightweight base
FROM python:3.12-slim

# 2. Optimization: Prevent python from buffering stdout (logs appear faster)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set work directory
WORKDIR /app

# 4. System dependencies (kept your git addition)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python deps (Cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
# Using '.' matches the WORKDIR.
COPY . .

# 7. Expose Port
EXPOSE 5050

# 8. Start command
# We explicitly call the module from the current directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050", "--reload"]
```

### File: `docker-compose.yml`
```python
services:
  rag_app:
    build: .
    container_name: agy_rag_backend
    ports:
      - "5050:5050"
    env_file:
      - .env
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - .:/app
      - ./data/chroma_db:/app/data/chroma_db
    # 🚀 NEW: Unlock hardware for AI workloads
    shm_size: '8gb'
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]
    # Changed to 'no' temporarily so you can see errors without infinite loops
    restart: "no"

```

### File: `.env.example`
*Not Found*
