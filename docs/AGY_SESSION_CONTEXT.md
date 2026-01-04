
# AntiGravity RAG - Session Context
**Generated:** 2026-01-02 20:10:00
**System:** Dual-GPU Omni-RAG (Titan RTX + GTX 1060)
**App State:** Docker Microservices v4.0


---

# AGY_HARDWARE_CTX.md (v2 - Professional Standard)
# USAGE: PASTE INTO GEMINI SYSTEM INSTRUCTIONS

### ROLE
You are the **AntiGravity Architect**, an expert AI partner for the "AntiGravity RAG" project.
* **Tone:** High-bandwidth, concise, "Anti-Fluff".
* **Method:** Analyze `AGY_SESSION_CONTEXT.md` before answering.

### CORE DIRECTIVE: TDD & SOLID
1.  **TEST FIRST (The Red-Green-Refactor Loop):**
    * **Never** generate implementation code without first generating a *failing* test case (The Probe).
    * **Step 1:** Generate `tests/test_feature_X.py`.
    * **Step 2:** User runs test (FAILS).
    * **Step 3:** Generate `app/feature_X.py` to satisfy test.
    * **Step 4:** User runs test (PASSES).
2.  **SOLID ARCHITECTURE:**
    * **SRP (Single Responsibility):** Each module does *one* thing (e.g., `safety.py` judges, `reflex.py` acts).
    * **IoC (Inversion of Control):** Dependencies are injected, not hardcoded. The `container.py` is the Source of Truth.
    * **Dry:** Don't Repeat Yourself.

### HARDWARE REALITY (STRICT)
* **Host:** Windows 10 Pro / WSL2 (Ubuntu).
* **GPU:** NVIDIA Titan RTX (24GB VRAM) - Passthrough enabled.
* **RAM:** 48GB Physical -> **32GB Allocated to WSL2** (Hard Limit).
* **CPU:** AMD Ryzen 5 1600 -> **8 vCPUs Allocated**.

### SECURITY PROTOCOLS
* **Gatekeeper:** You cannot execute code. You must provide `bash` or `python` scripts.
* **Secret Safety:** NEVER generate code with hardcoded secrets. Use `os.getenv()`.
* **Validation:** Review all generated code for syntax errors before outputting.

### OUTPUT FORMAT
* Use **Quadruple Backticks** (````) for all markdown artifacts containing code.
* Always end response with the immediate next execution step.


---

### 3. STRATEGIC ROADMAP (The Docker Evolution)
**STATUS: Task One (VectorStore) is currently ON HOLD.**

#### PHASE 1: THE MEMORY (Current Focus)
* [x] **Infrastructure:** Provision `chroma_db` container.
* [x] **Connection:** Verify Network Link (Brain -> Memory).
* [ ] **Software:** Implement `VectorStore` class [ON HOLD]
* [ ] **Verification:** Pass `tests/test_memory_logic.py`.
* [ ] **Feature:** "Ingest" - Build the document reader (`app/ingest.py`).

#### PHASE 2: THE AMNESIA FIX (Next Session)
* **Goal:** Eliminate file-based SQLite state.
* **Action:** Replace `chat_history.db` with a `postgres` container.
* **Why:** Concurrency support and data safety. If the container dies, the conversation survives.

#### PHASE 3: THE BRAIN TRANSPLANT (Future)
* **Goal:** Eliminate host-dependency on Ollama.
* **Action:** Move L1 (Ollama) into a Docker service with GPU passthrough.
* **Why:** True portability. The project becomes "Run anywhere," not "Run on Dan's specific Windows setup."

#### BACKLOG / TECH DEBT
* **Protocol Mismatch:** [RESOLVED] All layers now use `<reflex action="git_sync">`.
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.


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
            001_core_architecture.md
            003_security_gatekeeper.md
            AGY_SYSTEM_SPEC.md
            established per Function Cycle.md
            TO DO.md
            DansRig.md
            ROADMAP.md
            dan's updated rig
            005_development_protocols.md
            004_hardware_operations.md
            explanationOfBigPictureWithListOfTheParts.md
            002_vector_memory.md
            000_MASTER_OVERVIEW.md
            initialAgySetupChat
            AntiGravityDevPlan.md
        rag_local/
        app/
            config.py
            interfaces.py
            main.py
            safety.py
            ingestor.py
            L1_local.py
            L2_network.py
            database.py
            system_log.py
            router.py
            reflex.py
            container.py
            memory.py
        tests/
            test_L3_google.py
            test_protocol_e2e.py
            test_L2_connection.py
            test_L2_config.py
            test_ioc_refactor.py
            test_infra_connection.py
            test_3L_pipeline.py
            test_L1_fail.py
            test_ioc_baseline.py
            test_memory_logic.py
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
## 4. CRITICAL SOURCE CODE

### File: `app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .router import router as chat_router
from .config import config
from .container import container

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Verify L1 Model is pulled and ready
    print(f"🚀 AGY Starting up... Target L1: {config.L1_MODEL}")
    
    # Check health of the L1 driver via container
    is_ready = await container.l1_driver.check_health()
    if not is_ready:
        print("⚠️ WARNING: L1 Backend (Ollama) not responding. L1 calls will fail or escalate.")
    yield
    # SHUTDOWN
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
        "active_L1_model": config.L1_MODEL,
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
    L3_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
    L3_MODEL: str = "gemini-3-pro-preview"

    # === MEMORY (Chroma Docker) ===
    CHROMA_URL: str = "http://chroma_db:8000" 
    CHROMA_COLLECTION: str = "agy_knowledge"

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
        
    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[Config Error: DeepInfra API Key missing]"

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

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.base_url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    error_msg = f"DeepInfra Error {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    return f"[{error_msg}]"

                data = response.json()
                return data['choices'][0]['message']['content']

        except Exception as e:
            logger.error(f"L2 Connection Failed: {e}")
            return f"[L2 Connection Error: {str(e)}]"

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

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📨 USER: {request.message}")

    # 1. LAYER 1: LOCAL GENERATION (The Reflex)
    # L1 handles simple commands and basic chat.
    l1_response = await container.l1_driver.generate(request.message)
    
    # 2. PARSE ACTION (Unified)
    action_type, payload = parse_reflex_action(l1_response)
    
    # 3. INTERCEPT & EXECUTE
    if action_type:
        logger.info(f"⚡ ACTION DETECTED: {action_type}")
        if action_type == "git_sync":
            result = await execute_git_sync(payload) 
            return {"response": f"🤖 **Git Sync Triggered:**\n\n{result}"}
        
        # If shell/write came from L1 (unlikely but possible), handle them
        if action_type == "shell":
            result = await execute_shell(payload)
            return {"response": result}
        elif action_type == "write":
            path, content = payload
            result = await write_file(path, content)
            return {"response": result}

    # 4. ESCALATION CHECK
    # If L1 says ESCALATE, returns an error, or is too short, we go to L2
    if "ESCALATE" in l1_response or "L1 Error" in l1_response or len(l1_response) < 2:
        logger.info("🚀 ESCALATING TO L2...")
        system_hint = (
            "You are an Agentic AI. You can execute commands. "
            "To run shell: <reflex action=\"shell\">command</reflex> "
            "To write file: <reflex action=\"write\" path=\"filename\">content</reflex> "
            "To save work: <reflex action=\"git_sync\">Commit Message</reflex>"
        )
        full_prompt = f"{system_hint}\nUser: {request.message}"
        l2_response = await container.l2_driver.generate(full_prompt)
        
        # Parse potential L2 actions
        l2_action, l2_payload = parse_reflex_action(l2_response)
        if l2_action:
             if l2_action == "git_sync":
                 sync_result = await execute_git_sync(l2_payload)
                 return {"response": sync_result}
             elif l2_action == "shell":
                 result = await execute_shell(l2_payload)
                 return {"response": result}
             elif l2_action == "write":
                 path, content = l2_payload
                 result = await write_file(path, content)
                 return {"response": result}
        
        return {"response": l2_response}

    return {"response": l1_response}
```

### File: `app/memory.py`
```python
import logging
import sqlite3
import os
import chromadb
from datetime import datetime
from sentence_transformers import SentenceTransformer
from .config import config

logger = logging.getLogger("AGY_MEMORY")

# --- SQLITE: SHORT-TERM CONVERSATION HISTORY ---
DB_FILE = "chat_history.db"

def init_sqlite():
    """Ensures the local chat history database exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, role TEXT, content TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

# Initialize immediately on module load
init_sqlite()

async def save_interaction(role: str, content: str):
    """Saves a single message to SQLite history."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO history (role, content, timestamp) VALUES (?, ?, ?)", 
                  (role, content, datetime.now()))
        
        # Prune old history (Configurable limit)
        limit = 25 # Hardcoded or fetch from config
        c.execute(f"DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT {limit})")
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"❌ HISTORY ERROR: {e}")

async def retrieve_short_term_memory() -> str:
    """Retrieves recent chat history formatted for the LLM."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"SELECT role, content FROM history ORDER BY id ASC")
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            return ""
            
        history_text = "\n".join([f"{r[0].upper()}: {r[1]}" for r in rows])
        return f"--- CHAT HISTORY ---\n{history_text}\n"
    except Exception as e:
        logger.error(f"❌ RETRIEVE ERROR: {e}")
        return ""

# --- CHROMA: LONG-TERM VECTOR MEMORY ---
class VectorStore:
    def __init__(self):
        """
        Initializes connection to ChromaDB Docker Service & Local Embedder.
        """
        # 1. Connect to Docker Service (Not local file!)
        logger.info(f"🔌 CONNECTING TO MEMORY at {config.CHROMA_URL}...")
        try:
            self.client = chromadb.HttpClient(
                host="chroma_db", # Internal docker hostname
                port=8000
            )
            
            # 2. Get/Create Collection
            self.collection = self.client.get_or_create_collection(
                name=config.CHROMA_COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("✅ VECTOR DB CONNECTED.")
        except Exception as e:
            logger.error(f"❌ VECTOR DB FAILURE: {e}")
            raise e

        # 3. Load Embedding Model (Runs on GPU if available)
        logger.info("🧠 LOADING EMBEDDING MODEL (all-MiniLM-L6-v2)...")
        try:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ EMBEDDING MODEL READY.")
        except Exception as e:
            logger.critical(f"❌ MODEL LOAD FAILED: {e}")
            raise e

    def add_texts(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        """Embeds and saves text chunks."""
        if not texts: return

        try:
            embeddings = self.embedder.encode(texts).tolist()
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"💾 MEMORY: Stored {len(texts)} chunks.")
        except Exception as e:
            logger.error(f"❌ ADD ERROR: {e}")

    def search(self, query: str, n_results=5) -> list[str]:
        """Embeds query and searches Chroma."""
        try:
            query_embedding = self.embedder.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"❌ SEARCH ERROR: {e}")
            return []
```

### File: `app/container.py`
```python
import logging
from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import DeepInfraDriver
from .memory import VectorStore, save_interaction, retrieve_short_term_memory
from .ingestor import DocumentIngestor

logger = logging.getLogger("AGY_CONTAINER")

class Container:
    """
    The IoC Container (Switchboard).
    """
    def __init__(self):
        logger.info("🔧 INTIALIZING DEPENDENCY CONTAINER...")
        
        # 1. LAYER 1: LOCAL REFLEX (Ollama)
        self.l1_driver = LocalLlamaDriver(config=config)

        # 2. LAYER 2: REASONING (DeepInfra)
        self.l2_driver = DeepInfraDriver(
            api_key=config.L2_KEY,
            base_url=config.L2_URL,
            model=config.L2_MODEL
        )
        
        # 3. MEMORY: VECTOR STORE (Chroma)
        try:
            self.memory = VectorStore()
        except Exception as e:
            logger.error(f"⚠️ RUNNING WITHOUT VECTOR MEMORY: {e}")
            self.memory = None
            
        # 4. INGESTOR
        if self.memory:
            self.ingestor = DocumentIngestor(self.memory)
        else:
            self.ingestor = None
            
        logger.info("✅ CONTAINER READY.")

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
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - HF_HOME=/app/data/.huggingface
    volumes:
      - .:/app
      - ./data/huggingface:/app/data/.huggingface
    depends_on:
      - chroma_db
    shm_size: '8gb'
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]
    restart: "no"

  # SERVICE 2: THE MEMORY (Vector Store)
  chroma_db:
    image: chromadb/chroma:latest
    container_name: agy_chroma
    volumes:
      - ./data/chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
    ports:
      - "8000:8000"
    networks:
      default:

```

### File: `.env.example`
*Not Found*
