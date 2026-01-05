
# Gravitas Grounded Research - Session Context
**Generated:** 2026-01-04 19:05:52
**System:** Titan RTX (Local) + DeepInfra (Cloud)
**App State:** Docker Microservices


---
## HARDWARE OPERATIONS

# 004_HARDWARE_OPERATIONS.md
# STATUS: ACTIVE
# VERSION: 4.0.0 (Gravitas Grounded Research / Dual-GPU)

## 1. DUAL-GPU ARCHITECTURE
The system leverages **dual NVIDIA GPUs** for parallel processing and optimal resource utilization.

*   **GPU 0 (Titan RTX 24GB):** Primary Compute / Generation
    * **Role:** Dedicated AI Inference / Local LLM (L1) / Training
    * **Services:** `Gravitas_ollama` (Port 11434)
    * **Models:** `gemma2:27b-instruct-q4_k_m` (~17GB VRAM)

*   **GPU 1 (GTX 1060 6GB):** Dedicated Embedding Engine
    * **Role:** Runs productive workloads instead of idle display duty
    * **Services:** `Gravitas_ollama_embed` (Port 11435)
    * **Models:** `nomic-embed-text-v1.5`, `BAAI/bge-m3`, `BAAI/bge-reranker-v2-m3`

## 2. VRAM OVERLOAD PROTECTION
To prevent system crashes or OOM (Out Of Memory) during long context sessions, the system implements **OverloadError** exceptions:

1.  **Strict Buffer:** 2GB must remain free at all times.
2.  **Logic:** Prior to any L1 inference, `GPUtil` queries all GPUs.
3.  **Action:** If `Free_VRAM < 2GB` on any GPU, the request **must** be promoted to L2 to avoid crash.
4.  **Telemetry:** All VRAM checks logged to Postgres for monitoring and analysis.

## 3. MICROSERVICES TOPOLOGY
The system runs in a multi-container environment with dedicated services:

*   **`Gravitas_mcp`:** Main application container with sleep infinity for manual process injection
*   **`Gravitas_ollama`:** L1 model hosting (GPU 0 - Titan RTX)
*   **`Gravitas_ollama_embed`:** Embedding models (GPU 1 - GTX 1060)
*   **`Gravitas_qdrant`:** Hybrid vector database (CPU)
*   **`Gravitas_minio`:** Object storage for raw documents (CPU)
*   **`postgres_db`:** Chat history and telemetry logging (CPU)

## 4. ADVANCED HARDWARE FEATURES
* **Parallel Processing:** Embeddings don't block generation
* **VRAM Optimization:** Frees 6-7GB on Titan RTX for larger context
* **Cost Efficiency:** GTX 1060 runs productive workloads instead of idle display duty
* **Circuit Breaker:** GPU embedding with CPU fallback for resilience


---
## STRATEGIC ROADMAP

### 3. STRATEGIC ROADMAP (The Docker Evolution)

#### PHASE 1: THE MEMORY (COMPLETED)
* [x] **Infrastructure:** Provision `chroma_db` container.
* [x] **Connection:** Verify Network Link (Brain -> Memory).
* [x] **Software:** Implement `VectorStore` class.
* [x] **Verification:** Pass `tests/test_memory_logic.py`.
* [x] **Feature:** "Ingest" - Build the document reader (`app/ingest.py`).

#### PHASE 2: THE AMNESIA FIX (COMPLETED)
* [x] **Goal:** Eliminate file-based SQLite state.
* [x] **Infra:** Provision `postgres_db` container.
* [x] **Software:** Implement `app/database.py` (Async PG Driver).
* [x] **Verification:** History survives container restart.

#### PHASE 3: THE BRAIN TRANSPLANT (COMPLETED)
* **Goal:** Eliminate host-dependency on Ollama.
* **Action:** Move L1 (Ollama) into a Docker service with GPU passthrough.
* **Why:** True portability. The project becomes "Run anywhere."

#### BACKLOG / TECH DEBT
* **Terminology Governance:** Create a "Variable Name Document" to define project-wide naming standards (Gravitas vs. Legacy) and implement a validation script to ensure consistency across docs and code.
* **Protocol Mismatch:** [RESOLVED] All layers now use `<reflex action="git_sync">`.
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.


---
## PHYSICAL FILE MAP
```text
rag_local/
    penguins.csv
    test_l1.py
    t3.txt
    Gravitas_Grounded_Research.md
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
    test_cline_demo.txt
    .env
    dashboard.log
    .dockerignore
    Dockerfile
    memory.db
    chat_history.db
    testResults1.txt
    who_am_i.txt
    rag_local.code-workspace
    log_conf.yaml
    CHANGELOG.md
    _edit_bashrc
    .env.example
    test_memory.txt
        tools/
            switch_brain.py
        docs/
            TEST_GUIDE.md
            001_core_architecture.md
            AGY_SESSION_CONTEXT.md.bak
            todo9.md
            003_security_gatekeeper.md
            DansRig.md.bak
            HOWTO_DEV_REMINDERS.md
            established per Function Cycle.md.bak
            Gravitas Grounded Research Model Integration Technical Dump.md.bak
            established per Function Cycle.md
            TEST_GUIDE.md.bak
            Gravitas Grounded Research Model Integration Technical Dump.md
            DansRig.md
            completed_phase9.md
            TEST_AUDIT.md
            HOWTO_DEV_REMINDERS.md.bak
            ROADMAP.md
            developerNotes.md
            005_development_protocols.md
            004_hardware_operations.md
            004_hardware_operations.md.bak
            002_vector_memory.md
            000_MASTER_OVERVIEW.md
            Initial Context Prompt.md
        .clinerules/
            01-status-and-audit.md
            03-base-rules.md
            02-dev-workflow.md
            00-identity-and-hardware.md
        app/
            config.py
            mcp_server.py
            interfaces.py
            main.py
            safety.py
            simple_mcp.py
            ingestor.py
            L1_local.py
            L3_google.py
            exceptions.py
            L2_network.py
            database.py
            system_log.py
            telemetry.py
            storage.py
            router.py
            reflex.py
            container.py
            memory.py
            agents/
                librarian.py
                scout.py
            governance/
                inspector.py
                global_renamer.py
                accountant.py
        .agent/
            workflows/
        dashboard/
            app.js
            index.html
            style.css
        tests/
            test_mode_switching.py
            test_minio_storage.py
            test_L3_google.py
            test_l3_integration.py
            test_vram_safety.py
            test_ingestion_pipeline.py
            test_protocol_e2e.py
            test_L2_connection.py
            test_embed_breaker.py
            test_safety_logic.py
            test_telemetry.py
            test_hybrid_search.py
            test_inspector.py
            test_mcp_connection.py
            test_dual_gpu.py
            test_ioc_refactor.py
            test_infra_connection.py
            test_3L_pipeline.py
            test_ioc_baseline.py
            test_deepseek_sidecar.py
            test_nexus_api.py
            test_librarian.py
            test_memory_logic.py
            test_accountant.py
            test_memory_pruning.py
            test_reflex.py
            test_current_stack.py
        .vscode/
            sessions.json
        scripts/
            log_entry.py
            generate_context.py
            verify_chat.py
            load_knowledge.py
            ingest.py
            agy_writer.py
            audit_agy.sh
            test_ingestor.py
            warmup.py
            debug_import.py
            global_rename.py
            list_models.sh
            test_retrieval.py
            list_all_models.py
            router_refactored.py
            UpdateContext.py
            manage.py
            stats.py
            test_minio.py
            reset_agy.sh
            monitor.sh
            run_mcp.sh
            check_models.py
            debug_network.py
            init_db.sql
            titan_stress.py
            start_mcp.sh
            test_qwen3_connection.py
        .pytest_cache/
            .gitignore
            README.md
            CACHEDIR.TAG
            v/
                cache/
                    lastfailed
                    nodeids
```

---
## CRITICAL SOURCE CODE

### File: `app/main.py`
```python
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

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Gravitas Grounded Research",
    description="Dual-GPU Production-Grade Hybrid RAG Architecture",
    version="4.0.0",
    lifespan=lifespan
)

# MOUNT DASHBOARD (STATIC FILES)
dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
if os.path.exists(dashboard_path):
    app.mount("/dashboard", StaticFiles(directory=dashboard_path, html=True), name="dashboard")

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
```

### File: `app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # === GLOBAL IDENTITY ===
    USER_NAME: str = "Dan"
    PORT: int = 5050
    
    # === LAYER 1 (Local - Titan RTX) ===
    L1_URL: str = "http://ollama:11434"
    L1_MODEL: str = "codellama:7b"
    VRAM_THRESHOLD_GB: float = 2.0

    # === MODES (State Machine) ===
    MODE_RAG: str = "rag"
    MODE_DEV: str = "dev"
    DEFAULT_MODE: str = "rag"
    MODEL_MAP: dict[str, str] = {
        "rag": "gemma2:27b",
        "dev": "deepseek-coder-v2"
    }
    
    # === LAYER 2 (Cloud - Reasoning/Coding) ===
    L2_KEY: str | None = None
    L2_URL: str = "https://api.deepinfra.com/v1/openai/chat/completions"
    L2_MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"

    # === LAYER 3 (Agents - Google Gemini 3) ===
    L3_KEY: str | None = None
    L3_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
    L3_MODEL: str = "gemini-3-pro-preview"

    # === MEMORY & STORAGE (Gravitas Grounded Research) ===
    QDRANT_HOST: str = "agy_qdrant"
    QDRANT_PORT: int = 6333
    
    MINIO_ENDPOINT: str = "agy_minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "gravitas-blobs"
    MINIO_SECURE: bool = False

    # Deprecated (Chroma)
    CHROMA_URL: str = "http://chroma_db:8000" 
    CHROMA_COLLECTION: str = "agy_knowledge"
    DOCS_PATH: list[str] = [
        "/home/dflory/dev_env/rag_local/docs",
        "/home/dflory/dev_env/rag_local/app"
    ]

    # === DATABASE (Postgres) ===
    DB_HOST: str = "postgres_db"
    DB_PORT: int = 5432
    DB_USER: str = "agy_user"
    DB_PASS: str = "agy_pass"
    DB_NAME: str = "chat_history"

    # === GOVERNANCE (The Accountant) ===
    REF_COST_INPUT_1K: float = 0.0025
    REF_COST_OUTPUT_1K: float = 0.0100
    GRAVITAS_COST_KWH: float = 0.15

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Settings()

```

### File: `app/L1_local.py`
```python
import httpx
import logging
import GPUtil
from .interfaces import LLMDriver
from .config import Settings
from .telemetry import telemetry
from .exceptions import OverloadError

logger = logging.getLogger("AGY_L1")

class LocalLlamaDriver(LLMDriver):
    def __init__(self, config: Settings):
        self.base_url = config.L1_URL
        self.model_name = config.L1_MODEL
        self.timeout = 60.0

    async def load_model(self, model_name: str) -> bool:
        """Switches the active model and ensures it is available."""
        logger.info(f"🔄 Switching L1 model to: {model_name}")
        self.model_name = model_name
        return await self.ensure_model()

    async def generate(self, prompt: str) -> str:
        # Check VRAM before generation to prevent overload
        await self.check_vram()
        url = f"{self.base_url}/api/generate"
        
        # === SYSTEM INSTRUCTION ===
        # We wrap the user prompt to teach L1 about its new tool.
        system_prompt = (
            "You are the AntiGravity Assistant. You are a helpful, conversational coding expert.\n"
            "--- COMMANDS ---\n"
            "- To save work: <reflex action=\"git_sync\" />\n"
            "- To ESCALATE: If the user types '\\L2' at the start of their message or asks a deep logic/math question, reply ONLY with the word ESCALATE.\n"
            "--- BEHAVIOR ---\n"
            "For general questions like 'hello' or greetings, respond normally and do NOT include tags.\n\n"
            f"Context:\n{prompt}"
        )

        payload = {
            "model": self.model_name,
            "prompt": system_prompt, 
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    return f"[L1 Error: {response.status_code}]"

                data = response.json()
                raw_response = data.get("response", "").strip()
                
                # --- STATS CAPTURE ---
                from .database import db
                prompt_tokens = data.get("prompt_eval_count", 0)
                completion_tokens = data.get("eval_count", 0)
                # Ollama duration is in nanoseconds
                duration_ms = data.get("total_duration", 0) // 1_000_000 
                
                await db.log_usage(
                    model=self.model_name,
                    layer="L1",
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    duration_ms=duration_ms
                )
                
                # Cleanup: Sometimes 7b models add extra spaces or quotes
                if '<reflex action="git_sync"' in raw_response:
                    return '<reflex action="git_sync" />'
                
                return raw_response

        except Exception as e:
            return f"[L1 Error: {str(e)}]"

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(self.base_url)
                return resp.status_code == 200
        except:
            return False

    async def ensure_model(self) -> bool:
        """Checks if model exists, if not, pulls it."""
        check_url = f"{self.base_url}/api/tags"
        pull_url = f"{self.base_url}/api/pull"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Check if exists
                resp = await client.get(check_url)
                if resp.status_code == 200:
                    models_data = resp.json().get('models')
                    if models_data:
                        models = [m['name'] for m in models_data]
                        if self.model_name in models or f"{self.model_name}:latest" in models:
                            logger.info(f"✅ Model {self.model_name} already present.")
                            return True
                
                # 2. Pull if missing
                logger.info(f"📥 Pulling model {self.model_name} (this may take a while)...")
                await client.post(pull_url, json={"name": self.model_name, "stream": False}, timeout=300.0)
                return True
        except Exception as e:
            logger.error(f"❌ Failed to ensure model: {e}")
            return False

    async def check_vram(self) -> dict:
        """
        Check VRAM usage and implement overload protection.
        
        Returns:
            dict: VRAM information including total, used, and free memory per GPU
            
        Raises:
            OverloadError: If free VRAM is less than 2GB on any GPU
        """
        try:
            gpus = GPUtil.getGPUs()
            vram_info = []
            
            for gpu in gpus:
                total_vram = gpu.memoryTotal / 1024  # Convert to GB
                used_vram = gpu.memoryUsed / 1024
                free_vram = gpu.memoryFree / 1024
                
                gpu_info = {
                    'id': gpu.id,
                    'total_gb': round(total_vram, 2),
                    'used_gb': round(used_vram, 2),
                    'free_gb': round(free_vram, 2)
                }
                vram_info.append(gpu_info)
                
                # Log VRAM check
                await telemetry.log(
                    event_type="VRAM_CHECK",
                    component="L1",
                    value=free_vram,
                    metadata={
                        'gpu_id': gpu.id,
                        'total_vram_gb': total_vram,
                        'used_vram_gb': used_vram
                    },
                    status="OK"
                )
                
                # Check for overload condition
                if free_vram < 2.0:  # Less than 2GB free
                    await telemetry.log(
                        event_type="VRAM_LOCKOUT",
                        component="L1",
                        value=free_vram,
                        metadata={
                            'gpu_id': gpu.id,
                            'total_vram_gb': total_vram,
                            'used_vram_gb': used_vram
                        },
                        status="ERROR"
                    )
                    raise OverloadError(
                        message=f"VRAM overload detected on GPU {gpu.id}: {free_vram:.2f}GB free < 2GB threshold",
                        resource_type="VRAM",
                        current_value=free_vram,
                        threshold=2.0
                    )
            
            return vram_info
            
        except OverloadError:
            # Re-raise overload errors
            raise
        except Exception as e:
            logger.error(f"❌ VRAM CHECK FAILED: {e}")
            # Don't raise exception for monitoring failures, just log and continue
            return []

```

### File: `app/L2_network.py`
```python
import httpx
import logging
from .interfaces import LLMDriver

logger = logging.getLogger("AGY_L2")

class DeepInfraDriver(LLMDriver):
    """
    Dedicated Driver for DeepInfra (L2 Reasoning Layer).
    Strictly follows OpenAI-compatible API format.
    """
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model
        
    async def load_model(self, model_name: str) -> bool:
        """Updates the target model for L2."""
        logger.info(f"🔄 Switching L2 model to: {model_name}")
        self.model_name = model_name
        return True

    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "❌ CONFIG ERROR: DeepInfra API Key missing in `.env`."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # DeepInfra / OpenAI Standard Payload
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a precise Senior Python Engineer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2, # Low temp for coding precision
            "max_tokens": 2048
        }

        # RETRY CONFIG
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(self.base_url, headers=headers, json=payload)
                    
                    # 1. Success
                    if response.status_code == 200:
                        data = response.json()
                        
                        # --- STATS CAPTURE ---
                        from .database import db
                        usage = data.get("usage", {})
                        await db.log_usage(
                            model=self.model_name,
                            layer="L2",
                            prompt_tokens=usage.get("prompt_tokens", 0),
                            completion_tokens=usage.get("completion_tokens", 0),
                            duration_ms=0 
                        )
                        return data['choices'][0]['message']['content']

                    # 2. Fatal Errors (Auth / Bad Request) - Do not retry
                    if 400 <= response.status_code < 500:
                        error_msg = f"L2 CLIENT ERROR {response.status_code}: {response.text}"
                        logger.error(error_msg)
                        return f"⚠️ {error_msg}"
                    
                    # 3. Server Errors (5xx) - Retry
                    logger.warning(f"⚠️ L2 RETRY {attempt+1}/{max_retries}: Server Error {response.status_code}")

            except httpx.RequestError as e:
                # 4. Connection Failures - Retry
                logger.warning(f"⚠️ L2 RETRY {attempt+1}/{max_retries}: Connection Failed ({e})")
            
            # Backoff for next attempt (only if we haven't exhausted retries)
            if attempt < max_retries - 1:
                import asyncio
                await asyncio.sleep(base_delay * (2 ** attempt)) # 1s, 2s, 4s...

        # Final Failure
        logger.error("❌ L2 FAILED after all retries.")
        return "⚠️ L2 UNAVAILABLE: Connection to DeepInfra reasoning layer failed after multiple retries. Please check your internet connection."

    async def check_health(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 10
```

### File: `app/router.py`
```python
import logging
import re
from fastapi import APIRouter
from pydantic import BaseModel

from .container import container
from .reflex import execute_shell, write_file, execute_git_sync
from .config import config

logger = logging.getLogger("AGY_ROUTER")

class ChatRequest(BaseModel):
    message: str

class ModeRequest(BaseModel):
    mode: str

class ResearchRequest(BaseModel):
    query: str

router = APIRouter()

def parse_reflex_action(response_text: str):
    """
    Robustly scans response for XML-style reflex tags.
    Supports both <reflex action="..."/> (self-closing) and 
    <reflex action="...">content</reflex> formats.
    """
    # 1. Check for Shell Command
    shell_match = re.search(r'<reflex action="shell">(.*?)</reflex>', response_text, re.DOTALL)
    if shell_match:
        return "shell", shell_match.group(1).strip()
    
    # 2. Check for File Write
    write_match = re.search(r'<reflex action="write" path="(.*?)">(.*?)</reflex>', response_text, re.DOTALL)
    if write_match:
        path = write_match.group(1).strip()
        content = write_match.group(2).strip()
        return "write", (path, content)

    # 3. Check for Git Sync (Supports both formats)
    git_match_full = re.search(r'<reflex action="git_sync">(.*?)</reflex>', response_text, re.DOTALL)
    if git_match_full:
        return "git_sync", git_match_full.group(1).strip()
    
    if '<reflex action="git_sync"' in response_text:
        return "git_sync", "Automated sync from system."

    return None, None

def strip_reflex_tags(text: str) -> str:
    """
    Removes all <reflex> tags from the response text to leave only the conversational chat.
    """
    # Remove full tags with content
    text = re.sub(r'<reflex action=".*?">.*?</reflex>', '', text, flags=re.DOTALL)
    # Remove self-closing tags
    text = re.sub(r'<reflex action=".*?"\s*/>', '', text)
    return text.strip()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📨 USER: {request.message}")

    # 1. FORCED ESCALATION CHECK
    forced_escalate = request.message.strip().startswith("\\L2")
    l1_response = ""

    # --- SAVE USER MESSAGE TO HISTORY ---
    from .database import db
    if not forced_escalate:
        await db.save_history("user", request.message)
    
    # 0. RETRIEVAL (RAG)
    context_hint = ""
    if container.memory:
        try:
            docs = container.memory.search(request.message, n_results=3)
            if docs:
                context_hint = "--- KNOWLEDGE BASE ---\n" + "\n".join(docs) + "\n\n"
                logger.info(f"🧠 RAG: Retrieved {len(docs)} chunks.")
        except Exception as e:
            logger.error(f"⚠️ RAG SEARCH FAILED: {e}")

    # 1. LAYER 1: LOCAL GENERATION (The Reflex)
    # Skip L1 if we are forcing escalation
    if forced_escalate:
        l1_response = "ESCALATE"
    else:
        l1_response = await container.l1_driver.generate(f"{context_hint}{request.message}")
    
    # 2. PARSE ACTION (Unified)
    action_type, payload = parse_reflex_action(l1_response)
    clean_l1_text = strip_reflex_tags(l1_response)
    
    # 3. INTERCEPT & EXECUTE
    if action_type:
        logger.info(f"⚡ ACTION DETECTED: {action_type}")
        result_msg = ""
        if action_type == "git_sync":
            sync_result = await execute_git_sync(payload) 
            result_msg = f"🤖 **Git Sync Triggered:**\n\n{sync_result}"
        elif action_type == "shell":
            result_msg = await execute_shell(payload)
        elif action_type == "write":
            path, content = payload
            result_msg = await write_file(path, content)

        final_msg = f"{clean_l1_text}\n\n{result_msg}".strip()
        return {"response": final_msg, "layer": "L1"}

    # 4. ESCALATION CHECK
    # If L1 says ESCALATE, returns an error, or is too short, we go to L2
    if "ESCALATE" in l1_response or "L1 Error" in l1_response or len(l1_response) < 2:
        logger.info("🚀 ESCALATING TO L2 (with History)...")
        
        # --- CONTEXT BUILDING (History) ---
        from .database import db
        history_rows = await db.get_recent_history(limit=5)
        history_block = ""
        if history_rows:
            history_block = "--- RECENT CONVERSATION HISTORY ---\n"
            for h in history_rows:
                history_block += f"{h['role'].upper()}: {h['content']}\n"
            history_block += "---\n\n"

        system_hint = (
            "You are an Agentic AI with Full Situational Awareness. "
            "Use the conversation history and knowledge base provided to give the best answer. "
            "To run shell: <reflex action=\"shell\">command</reflex> "
            "To write file: <reflex action=\"write\" path=\"filename\">content</reflex> "
            "To save work: <reflex action=\"git_sync\">Commit Message</reflex>\n\n"
        )
        
        # If forced, strip the trigger word from the prompt we send to L2
        actual_msg = request.message
        if forced_escalate:
            actual_msg = actual_msg.replace("\\L2", "", 1).strip()

        full_prompt = f"{system_hint}{history_block}{context_hint}User: {actual_msg}"
        l2_response = await container.l2_driver.generate(full_prompt)
        
        # Parse potential L2 actions
        l2_action, l2_payload = parse_reflex_action(l2_response)
        clean_l2_text = strip_reflex_tags(l2_response)

        if l2_action:
             result_msg = ""
             if l2_action == "git_sync":
                 sync_result = await execute_git_sync(l2_payload)
                 result_msg = sync_result
             elif l2_action == "shell":
                 result_msg = await execute_shell(l2_payload)
             elif l2_action == "write":
                 path, content = l2_payload
                 result_msg = await write_file(path, content)
            
             final_msg = f"{clean_l2_text}\n\n{result_msg}".strip()
             await db.save_history("ai", final_msg)
             return {"response": final_msg, "layer": "L2"}
        
        await db.save_history("ai", l2_response)
        return {"response": l2_response, "layer": "L2"}

    await db.save_history("ai", l1_response)
    return {"response": l1_response, "layer": "L1"}

@router.post("/ingest")
async def trigger_ingestion():
    """
    Manually triggers the Document Ingestor.
    """
    if not container.ingestor:
        return {"status": "error", "message": "Ingestor not initialized (Vector Store missing?)"}
    
    try:
        # We run this in a background task if it's large, but for now blocking is okay for a dev tool
        await container.ingestor.ingest_all()
        return {"status": "success", "message": "Knowledge ingestion complete."}
    except Exception as e:
        logger.error(f"❌ INGESTION ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.delete("/history")
async def clear_chat_history():
    """
    Clears the short-term chat history from the database.
    """
    try:
        from .database import db
        count = await db.clear_history()
        return {"status": "success", "message": f"Chat history cleared ({count} messages purged)."}
    except Exception as e:
        logger.error(f"❌ CLEAR HISTORY ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/stats/summary")
async def get_stats_summary():
    """
    Returns a high-level summary of usage statistics for the dashboard.
    """
    try:
        from .database import db
        if not db.pool:
            return {"status": "error", "message": "Database not connected"}
            
        async with db.pool.acquire() as conn:
            totals = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(prompt_tokens) as total_prompt,
                    SUM(completion_tokens) as total_completion,
                    AVG(duration_ms) as avg_latency,
                    SUM(CASE WHEN layer = 'L2' THEN prompt_tokens + completion_tokens ELSE 0 END) as l2_tokens
                FROM usage_stats
            ''')
            
            breakdown = await conn.fetch('''
                SELECT model, layer, COUNT(*) as count
                FROM usage_stats
                GROUP BY model, layer
            ''')
            
            return {
                "status": "success",
                "summary": {
                    "total_requests": totals["total_requests"] or 0,
                    "total_tokens": (totals["total_prompt"] or 0) + (totals["total_completion"] or 0),
                    "l2_tokens": totals["l2_tokens"] or 0,
                    "avg_latency_ms": float(totals["avg_latency"] or 0),
                },
                "breakdown": [dict(row) for row in breakdown]
            }
    except Exception as e:
        logger.error(f"❌ STATS SUMMARY ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/health/detailed")
async def get_detailed_health():
    """
    Checks connectivity for all microservices and GPU stats.
    """
    from .database import db
    import subprocess
    
    health = {
        "api": "online",
        "postgres": "online" if db.is_ready() else "offline",
        "chroma": "offline",
        "ollama": "offline",
        "gpu": {"used": 0, "total": 0, "percentage": 0}
    }
    
    # Check Ollama
    if await container.l1_driver.check_health():
        health["ollama"] = "online"
        
    # Check Chroma
    try:
        if container.memory and container.memory.collection:
             health["chroma"] = "online"
    except:
        pass

    # Check GPU (NVIDIA)
    try:
        # Get first GPU's memory usage
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

class PullRequest(BaseModel):
    model: str

@router.post("/model/pull")
async def pull_model_endpoint(request: PullRequest):
    """
    Triggers an asynchronous model pull in the Ollama container.
    """
    try:
        # We temporarily change the driver's target model to the requested one
        old_model = container.l1_driver.model_name
        container.l1_driver.model_name = request.model
        
        # Trigger pull (non-blocking in our implementation)
        success = await container.l1_driver.ensure_model()
        
        # Revert driver model (the endpoint is for management, not permanent switch)
        container.l1_driver.model_name = old_model
        
        if success:
            return {"status": "success", "message": f"Pulling {request.model}..."}
        else:
            return {"status": "error", "message": f"Failed to initiate pull for {request.model}"}
    except Exception as e:
        logger.error(f"❌ MODEL PULL ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/system/mode")
async def switch_system_mode(request: ModeRequest):
    """
    Switches the system between RAG and DEV modes (Mutually Exclusive).
    """
    success = await container.switch_mode(request.mode)
    if success:
        return {
            "status": "success", 
            "message": f"System switched to {request.mode} mode.",
            "current_mode": container.current_mode,
            "model": container.l1_driver.model_name
        }
    else:
        return {"status": "error", "message": f"Failed to switch to {request.mode} mode."}

@router.get("/governance/financials")
async def get_financial_report():
    """
    Returns the ROI and savings report from the Cost Accountant.
    """
    try:
        from .governance.accountant import accountant
        report = await accountant.calculate_roi()
        return report
    except Exception as e:
        logger.error(f"❌ FINANCIALS ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/agents/librarian/run")
async def run_librarian():
    """
    Manually triggers the Librarian Agent to process the inbox.
    """
    try:
        result = await container.librarian.process_inbox()
        return result
    except Exception as e:
        logger.error(f"❌ LIBRARIAN ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/agents/scout/research")
async def scout_research(request: ResearchRequest):
    """
    Triggers the Scout Agent for Deep Research.
    """
    try:
        if not container.scout:
             return {"status": "error", "message": "Scout Agent not initialized."}
        
        report = await container.scout.research(request.query)
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"❌ SCOUT ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}
```

### File: `app/container.py`
```python
import logging
from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import DeepInfraDriver
from .L3_google import GoogleGeminiDriver
from .memory import QdrantVectorStore, save_interaction, retrieve_short_term_memory
from .storage import MinioConnector
from .ingestor import DocumentIngestor
from .telemetry import telemetry

logger = logging.getLogger("AGY_CONTAINER")

class Container:
    """
    The IoC Container (Switchboard).
    Updated for Gravitas Grounded Research Phase 4.1.
    """
    def __init__(self):
        logger.info("🔧 INITIALIZING DEPENDENCY CONTAINER (Gravitas Grounded Research Phase 4.1)...")
        
        # 1. LAYER 1: LOCAL REFLEX (Ollama)
        try:
            self.l1_driver = LocalLlamaDriver(config=config)
            logger.info("✅ L1 Driver (LocalLlama) READY.")
        except Exception as e:
            logger.error(f"❌ L1 Driver initialization failed: {e}")
            raise

        # 2. LAYER 2: REASONING (DeepInfra)
        try:
            self.l2_driver = DeepInfraDriver(
                api_key=config.L2_KEY,
                base_url=config.L2_URL,
                model=config.L2_MODEL
            )
            logger.info("✅ L2 Driver (DeepInfra) READY.")
        except Exception as e:
            logger.error(f"❌ L2 Driver initialization failed: {e}")
            raise

        # 3. LAYER 3: DEEP RESEARCH (Google Gemini)
        try:
            self.l3_driver = GoogleGeminiDriver(
                api_key=config.L3_KEY,
                model=config.L3_MODEL
            )
            logger.info("✅ L3 Driver (Google Gemini) READY.")
        except Exception as e:
            logger.error(f"❌ L3 Driver initialization failed: {e}")
            raise
        
        # 4. STORAGE: BLOB STORE (MinIO)
        try:
            self.storage = MinioConnector(
                endpoint=config.MINIO_ENDPOINT,
                access_key=config.MINIO_ACCESS_KEY,
                secret_key=config.MINIO_SECRET_KEY,
                bucket_name=config.MINIO_BUCKET,
                secure=config.MINIO_SECURE
            )
            logger.info("✅ STORAGE (MinIO) READY.")
        except Exception as e:
            logger.error(f"❌ STORAGE INIT FAILURE: {e}")
            self.storage = None

        # 5. MEMORY: VECTOR STORE (Qdrant)
        try:
            if self.storage:
                self.memory = QdrantVectorStore(
                    storage=self.storage,
                    host=config.QDRANT_HOST,
                    port=config.QDRANT_PORT
                )
                logger.info("✅ MEMORY (Qdrant) READY.")
            else:
                logger.warning("⚠️ Cannot initialize memory without valid storage connector.")
                self.memory = None
        except Exception as e:
            logger.error(f"⚠️ RUNNING WITHOUT VECTOR MEMORY: {e}")
            self.memory = None
            
        # 6. INGESTOR
        try:
            if self.memory and self.storage:
                self.ingestor = DocumentIngestor(
                    vector_store=self.memory, 
                    storage=self.storage
                )
                logger.info("✅ INGESTOR READY.")
            else:
                logger.warning("⚠️ Cannot initialize ingestor without valid memory and storage.")
                self.ingestor = None
        except Exception as e:
            logger.error(f"❌ INGESTOR INIT FAILURE: {e}")
            self.ingestor = None

        # 7. TELEMETRY
        try:
            self.telemetry = telemetry
            logger.info("✅ TELEMETRY READY.")
        except Exception as e:
            logger.error(f"❌ TELEMETRY INIT FAILURE: {e}")
            self.telemetry = None

        # 8. STATE MANAGEMENT
        self.current_mode = config.DEFAULT_MODE

        # 9. AGENTS: THE LIBRARIAN
        try:
            from .agents.librarian import LibrarianAgent
            self.librarian = LibrarianAgent(container=self)
            logger.info("✅ LIBRARIAN AGENT READY.")
        except Exception as e:
            logger.error(f"❌ LIBRARIAN AGENT INIT FAILURE: {e}")
            self.librarian = None

        # 10. AGENTS: THE SCOUT
        try:
            from .agents.scout import ScoutAgent
            self.scout = ScoutAgent(l3_driver=self.l3_driver, memory=self.memory)
            logger.info("✅ SCOUT AGENT READY.")
        except Exception as e:
            logger.error(f"❌ SCOUT AGENT INIT FAILURE: {e}")
            self.scout = None

        logger.info(f"✅ CONTAINER READY (Mode: {self.current_mode}).")

    async def switch_mode(self, target_mode: str) -> bool:
        """
        Mutually Exclusive Mode Switch (VRAM Management).
        """
        if target_mode == self.current_mode:
            logger.info(f"Already in {target_mode} mode.")
            return True
        
        # Resolve model name from config
        new_model = config.MODEL_MAP.get(target_mode)
        if not new_model:
            logger.error(f"Unknown mode: {target_mode}")
            return False
            
        logger.info(f"🔄 SWITCHING SYSTEM MODE: {self.current_mode} -> {target_mode}")
        
        # Switch model in L1
        success = await self.l1_driver.load_model(new_model)
        if success:
            self.current_mode = target_mode
            logger.info(f"✅ Mode switched to {target_mode}")
            return True
        else:
            logger.error(f"❌ Failed to switch mode to {target_mode}")
            return False

# Singleton Instance
container = Container()

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
# Version line removed to avoid the "obsolete" warning
services:
  # --- CORE: GRAVITAS MCP (THE TARGET) ---
  gravitas_mcp:
    container_name: gravitas_mcp
    build:
      context: .
      dockerfile: Dockerfile
    # CRITICAL FIX: "sleep infinity" keeps the container running 24/7.
    # Cline will inject the python process manually using 'docker exec'.
    command: [ "sleep", "infinity" ]
    volumes:
      - .:/app
    environment:
      - PYTHONPATH=/app
      - POSTGRES_HOST=postgres_db
      - QDRANT_HOST=agy_qdrant
      - OLLAMA_HOST=agy_ollama # GPU 0
      - OLLAMA_EMBED_HOST=agy_ollama_embed # GPU 1
      - MINIO_HOST=agy_minio
      # Ensure these match your .env
      - POSTGRES_USER=${DB_USER:-agy_user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-agy_pass}
      - POSTGRES_DB=${DB_NAME:-chat_history}
    ports:
      - "8001:8000" # Maps port 8000 inside to 8001 outside (just in case)
    depends_on:
      - postgres_db
      - qdrant
      - ollama
      - ollama_embed
    networks:
      - rag_net
    restart: unless-stopped

  # --- GPU 0: GENERATION (TITAN RTX) ---
  ollama:
    image: ollama/ollama:latest
    container_name: agy_ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: [ '0' ] # Titan RTX
              capabilities: [ gpu ]
    volumes:
      - ./data/ollama_models:/root/.ollama
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0
    networks:
      - rag_net
    restart: always

  # --- GPU 1: EMBEDDINGS (GTX 1060) ---
  ollama_embed:
    image: ollama/ollama:latest
    container_name: agy_ollama_embed
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: [ '1' ] # GTX 1060
              capabilities: [ gpu ]
    volumes:
      - ./data/ollama_embed_models:/root/.ollama
    ports:
      - "11435:11434" # Mapped to 11435 to avoid conflict with GPU 0
    environment:
      - OLLAMA_HOST=0.0.0.0
    networks:
      - rag_net
    restart: always

  # --- MEMORY: QDRANT (HYBRID VECTOR DB) ---
  qdrant:
    image: qdrant/qdrant:latest
    container_name: agy_qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./data/qdrant:/qdrant/storage
    environment:
      - QDRANT_ALLOW_RECOVERY_MODE=true
    networks:
      - rag_net
    restart: always

  # --- STORAGE: MINIO (OBJECT STORE) ---
  minio:
    image: minio/minio:latest
    container_name: agy_minio
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ./data/minio:/data
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"
    networks:
      - rag_net
    restart: always

  # --- DATABASE: POSTGRES (HISTORY) ---
  postgres_db:
    image: postgres:16-alpine
    container_name: postgres_db
    environment:
      - POSTGRES_USER=${DB_USER:-agy_user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-agy_pass}
      - POSTGRES_DB=${DB_NAME:-chat_history}
    volumes:
      - ./data/postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - rag_net
    restart: always

  # --- API: RAG BACKEND (LEGACY/ROUTER) ---
  rag_app:
    build: .
    container_name: agy_rag_backend
    # Optional: If you run the main app via uvicorn
    command: uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload
    volumes:
      - .:/app
    ports:
      - "5050:5050"
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-agy_user}:${DB_PASSWORD:-agy_pass}@postgres_db:5432/${DB_NAME:-chat_history}
      - DB_HOST=postgres_db
      - L1_URL=http://agy_ollama:11434
    depends_on:
      - postgres_db
      - qdrant
    networks:
      - rag_net

networks:
  rag_net:
    driver: bridge

```

### File: `.env.example`
```python
# === Identity ===
USER_NAME=Dan
PORT=5050

# === L1 (Titan RTX - Reflex) ===
L1_URL=http://127.0.0.1:11434
L1_MODEL=codellama:7b
VRAM_THRESHOLD_GB=2.0

# === L2 (Cloud - Reasoning/Coding) ===
L2_KEY=your_deepinfra_key_here
L2_URL=https://api.deepinfra.com/v1/openai/chat/completions
L2_MODEL=Qwen/Qwen3-Coder-480B-A35B-Instruct

# === L3 (Agents - Deep Research) ===
# Google Gemini 3 Pro (Agentic & Reasoning Flagship)
L3_KEY=your_google_gemini_key_here
# Updated to the v1beta endpoint which hosts the 'preview' models
L3_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent
L3_MODEL=gemini-3-pro-preview

# === Database ===
DB_USER=agy_user
DB_PASSWORD=agy_pass
DB_NAME=chat_history
# DB_HOST=localhost (Used in scripts/reset_agy.sh overrides)

```

### File: `scripts/monitor.sh`
```python
#!/bin/bash
# Gravitas Resource Watcher
# Monitors GPU VRAM and Docker Container overhead in real-time.

clear
echo "🚀 Initializing Gravitas Resource Watcher..."
echo "Press CTRL+C to stop."
sleep 1

while true; do
    # 1. Gather all data into a buffer first
    GPU_DATA=$(nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | \
    awk -F', ' '{printf "GPU %d: %-15s | VRAM (Used / Total): %4.1f / %4.1f GB | Real Load: %3s%%\n", $1, $2, $3/1024, $4/1024, $5}')
    
    DOCKER_DATA=$(docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep -v "gravitas_mcp")
    
    # Read heartbeat if it exists
    if [ -f /tmp/gravitas_heartbeat ]; then
        ACTIVE_FILE=$(cat /tmp/gravitas_heartbeat)
        # Only show last 50 chars of path
        DISPLAY_FILE="...${ACTIVE_FILE: -50}"
    else
        DISPLAY_FILE="IDLE"
    fi

    # 2. Now move cursor home and overwrite
    tput home
    echo "=========================================================================="
    echo "🧪 REFACTOR STATUS"
    echo "=========================================================================="
    echo "Active File: $DISPLAY_FILE"
    echo ""
    echo "=========================================================================="
    echo "📟 GPU TELEMETRY"
    echo "=========================================================================="
    echo "$GPU_DATA"
    
    echo ""
    echo "=========================================================================="
    echo "🐳 CONTAINER RESOURCE CONSUMPTION"
    echo "=========================================================================="
    echo "$DOCKER_DATA"
    
    echo ""
    echo "=========================================================================="
    echo "🕒 Last Updated: $(date '+%H:%M:%S')"
    echo "=========================================================================="
    
    # 3. Clear any leftover lines below
    tput ed
    
    sleep 1
done

```
