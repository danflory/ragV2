
# Gravitas Grounded Research - Session Context
**Generated:** 2026-01-05 18:52:13
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
4.  **Telemetry:** All VRAM checks and load/thought latency metrics logged to Postgres for monitoring and **Phase 5 Dynamic Governance**. 60-day history maintained via aggregation.

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

# GRAVITAS GROUNDED RESEARCH - STRATEGIC ROADMAP

## CURRENT STATE: v4.2.0 (GRAVITAS REBRAND & AGENTIC CONSTRUCTION)
The core infrastructure (Dockerized local RAG, Dual-GPU orchestration, Qdrant Memory + MinIO Storage, Postgres History) is stable. Agentic construction via Antigravity is active.

## COMPLETED PHASES

### PHASE 1: THE FOUNDATION (QDRANT & MINIO)
* [x] **Hybrid Storage:** Split vectors (Qdrant) from blobs (MinIO) for hardware efficiency.
* [x] **Verification:** Full ingestion and search pipeline verified in `tests/`.

### PHASE 2: PERSISTENCE & TELEMETRY
* [x] **Infrastructure:** Provisioned `Gravitas_postgres` for chat history and metrics.
* [x] **Telemetry:** Implemented `app/telemetry.py` for VRAM tracking and system events.

### PHASE 3: THE GRAVITAS EVOLUTION (REBRANDING)
* [x] **Consistency:** Global rename of all legacy "agy" / "AntiGravity" terms to **Gravitas**.
* [x] **Automation:** Hooked session context generation into the system startup.
* [x] **Protocols:** Established `docs/GRAVITAS_NOMENCLATURE.md` and `docs/005_development_protocols.md`.

---

## UPCOMING PHASES

### PHASE 4: COMMAND & CONTROL (THE NEXUS DASHBOARD)
* [x] **Master Control Dashboard:** Unified Web UI for service management, model pulling, and system resets. **Includes integrated VRAM and Docker health metrics via Server-Sent Events (SSE)** for real-time monitoring.
* [x] **Health API:** Implement `/health` endpoints for all containers to feed real-time status to the Nexus.


### PHASE 4.5: GRANULAR TELEMETRY CALIBRATION (THE SENSORS)
* [ ] **Sensor Implementation:** Upgrade `app/telemetry.py` to record sub-second metrics: **Load Latency** (VRAM setup) and **Thought Latency** (Inference Speed).
* [ ] **Weighted Telemetry Aggregation:** 
    * **Pre-Calculation**: Refactor logging logic to measure "Work Units" (Tokens Generated) *before* database entry.
    * **The Efficiency Score**: Store **Latency-Per-Token** (Weighted) rather than flat temporal averages to accurately reflected system strain under load.
* [ ] **The 60-Day Historic Window:** Establish a 60-day data retention policy in Postgres to track long-term hardware performance.
* [ ] **Safety (Aggregation & Monitoring):** 
    * **Aggregation**: Average the Weighted Efficiency Scores every 60s to prevent database bloat.
    * **Dashboard Widget**: Create a "Telemetry Footprint" monitor to track disk space used by the millions of potential hits.
    * **Auto-Pruning Logic**: Implement the 60-day pruning mechanism in `ANTIGRAVITY_Scripts/maintenance.py` (Deferred from initial setup, now placed here).

### PHASE 5: DYNAMIC MODEL GOVERNANCE (THE SUPERVISOR)
* [ ] **Data-Driven Dispatcher:** Use the 60 days of calibrated **Telemetry Data** to route tasks based on real-time load times, token speeds, and cost.
* [ ] **Predictive Context Orchestration:** Define acceptable context switching costs based on **Actual Historic Data** (e.g., loading a 70B model for a long work queue vs. rapid switching on a 6GB card).
* [ ] **Dynamic Trade-off Self-Correction:** Implement an autonomous feedback loop where the Supervisor audits its own scheduling decisions and automatically adjusts the routing plan.

### PHASE 6: SELF-LEARNING DATA (REASONING PIPES)
* [ ] **Reasoning Pipe Architecture:** Implement the standardized naming schema: `docs/journals/ReasoningPipe_{agentName}.md`.
* [ ] **Self-Improvement Foundation:** Establish these pipes as the primary dataset for future self-audit and capability evolution.
* [ ] **Buffer-Append Protocol:** Implement the "Zero-Editing" logic where an active session buffer is appended to the agent-specific ReasoningPipe upon session completion.
* [ ] **Action Visibility Trace:** Every agent, regardless of model internal reasoning capability, must log state-changes (e.g., "Modified file X") to ensure a complete audit trail.
* [ ] **14-Day Cycle**: Reasoning data remains active for 14 days for forensic and self-learning analysis.

### PHASE 7: ADVANCED KNOWLEDGE INDEXING
* [ ] **From Semantic Keys to Knowledge Indexes:** Refactor the ingestion pipeline toward structured, concept-aware indexing.
* [ ] **Hierarchical Summarization:** Deploy the **Gravitas Librarian** to generate "Big Picture" summaries of all local documentation.
* [ ] **Relational Mapping:** Implement entity extraction to map dependencies between code files and architectural decisions.

### PHASE 8: AGENT SPECIALIZATION (THE SCOUT'S EXPANSION)
* [ ] **Multimodal Transcription:** Integrate `yt-dlp` and `Whisper` to allow the **Gravitas Scout** to ingest YouTube and audio sermons.
* [ ] **Live Web Probing:** Implement live web search for the **Gravitas Scout**.
* [ ] **L3 Feedback Loop:** Formalize the **Gravitas Scout**'s ability to "Ask L3" iterative reasoning questions.

### PHASE 9: GRAVITAS AGENTIC INFRASTRUCTURE
* [ ] **Mirroring Construction Protocols**: Research and implement a `.gravitas_agent` directory for each Gravitas Agent (**Gravitas Scout**, **Gravitas Librarian**, etc.).
* [ ] **Standardized Startup**: Implement a `recon` phase for Gravitas Agents to ensure they sync with global project state.

### PHASE 10: INTELLIGENCE AUDIT & BENCHMARKING
* [ ] **Bi-Weekly Model Pulse:** Establish an automated sweep (every 14 days) of Ollama, DeepInfra, and Google for new model releases.
* [ ] **Independent Test Suite:** Develop a project-specific benchmarking suite to validate model performance against Gravitas RAG and code synthesis tasks before promotion to active roles.

---

## BACKLOG / TECH DEBT
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.
* [x] **Journal Rotation:** Implement dated journal snapshots for high-fidelity RAG ingestion. (Completed: `docs/journals/`)
* **VENV Hardening:** Standardize cross-platform dependency resolution in `requirements.txt`.


---
## PHYSICAL FILE MAP
```text
Gravitas/
    onArrival.txt
    .gitignore
    rag_memory.db
    gravitas_mcp_config.json
    READ_ME_GRAVITAS_MASTER_MANUAL.md
    docker-compose.yml
    requirements.txt
    .env
    .dockerignore
    Dockerfile
    log_conf.yaml
    debug_rag_retrieval.py
    CHANGELOG.md
    .env.example
        tools/
            switch_brain.py
        docs/
            TEST_GUIDE.md
            hardware_rig.md
            gemini_3_model_guide.md
            RAG_DEBUG_ANALYSIS.md
            001_core_architecture.md
            STRATEGY_SESSION_2026_01_04.md
            003_security_gatekeeper.md
            GOOGLE_ANTIGRAVITY_SPEC.md
            HOWTO_DEV_REMINDERS.md
            function_cycles.md
            COMPLETE_SESSION_SUMMARY.md
            TEST_RESULTS_INTEGRATED_RAG.md
            NEXUS_RESCAN_IMPROVEMENTS.md
            TEST_AUDIT.md
            SESSION_SUMMARY_RAG_TESTING.md
            ROADMAP.md
            developerNotes.md
            005_development_protocols.md
            004_hardware_operations.md
            GRAVITAS_NOMENCLATURE.md
            002_vector_memory.md
            FAQ.md
            model_integration.md
            000_MASTER_OVERVIEW.md
            Initial Context Prompt.md
            RAG_REFUSAL_RESOLUTION.md
            journals/
                2026-01-04_executive.md
                current_session.md
                2026-01-05_thoughts.md
                2026-01-05_executive.md
                2026-01-04_thoughts.md
            archived/
                todo9.md
                completed_phase9.md
            architecture/
                thinking_transparency.md
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
        temporaryTesting/
            2026-01-05_FileAccessAudit.md
            session_file_reads.md
        .agent/
            executive_template.md
            vocabulary.md
            workflows/
                log.md
                recon.md
                reason.md
        dashboard/
            app.js
            index.html
            style.css
        tests/
            test_rag_diagnostics.py
            test_mode_switching.py
            test_minio_storage.py
            test_L3_google.py
            test_l3_integration.py
            test_integrated_rag_prompts.py
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
            settings.json
        ANTIGRAVITY_Scripts/
            maintenance.py
            reasoning_pipe.py
        scripts/
            log_entry.py
            generate_context.py
            verify_chat.py
            load_knowledge.py
            ingest.py
            inventory.sh
            manual_ingest.py
            warmup.py
            debug_import.py
            global_rename.py
            list_all_models.py
            reset_gravitas.sh
            manage.py
            mcp_entrypoint.sh
            stats.py
            test_minio.py
            audit_gravitas.sh
            monitor.sh
            check_models.py
            debug_network.py
            sync_external_context.py
            init_db.sql
            titan_stress.py
            test_qwen3_connection.py
            experimental/
                test_ingest_v2.py
                test_minimal.py
                test_final_metal.py
                test_memory_ingest.py
                test_rag_v3.py
                v12_log.txt
                fix_memory.py
                test_ingest.py
                check_vram.py
                test_ingest_v5.py
                test_ingest_v11.py
                test_ingestor.py
                test_output_metal.log
                test_rag.py
                test_final.py
                test_retrieval.py
                ingest_v5_output.txt
                test_ingest_v6.py
                test_ingest_v4.py
                test_ingest_v10.py
                test_rag_v4.py
                test_output.log
                test_ingest_v8.py
                test_ingest_v12.py
                test_ingest_v9.py
                test_ingest_v7.py
                test_db.py
                test_sentence_transformers.py
                test_rag_diagnostics_results.txt
                test_ingest_v3.py
                test_rag_direct.py
                final_ingest_log.txt
                test_rag_query.py
                test_sentence_transformers_v2.py
                ingest_v8_output.txt
                test_rag_results.txt
                test_rag_v2.py
                test_ollama.py
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

if os.path.exists(dashboard_path):
    from fastapi.responses import FileResponse
    
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(dashboard_path, "index.html"))

    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")
```

### File: `app/config.py`
```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # === GLOBAL IDENTITY ===
    USER_NAME: str = "Dan"
    PORT: int = 5050
    
    # === LAYER 1 (Local - Titan RTX) ===
    L1_URL: str = "http://Gravitas_ollama:11434"
    L1_EMBED_URL: str = "http://Gravitas_ollama_embed:11434"
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
    QDRANT_HOST: str = "Gravitas_qdrant"
    QDRANT_PORT: int = 6333
    
    MINIO_ENDPOINT: str = "Gravitas_minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "gravitas-blobs"
    MINIO_SECURE: bool = False

    # Deprecated (Chroma)
    CHROMA_URL: str = "http://chroma_db:8000" 
    CHROMA_COLLECTION: str = "Gravitas_knowledge"
    DOCS_PATH: list[str] = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
    ]



    # === DATABASE (Postgres) ===
    DB_HOST: str = "Gravitas_postgres"
    DB_PORT: int = 5432
    DB_USER: str = "Gravitas_user"
    DB_PASS: str = "Gravitas_pass"
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

logger = logging.getLogger("Gravitas_L1")

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
            "You are the Gravitas Assistant. You are a helpful, conversational coding expert.\n"
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

logger = logging.getLogger("Gravitas_L2")

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
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx
from pydantic import BaseModel
import asyncio
import json
import subprocess

from .container import container
from .reflex import execute_shell, write_file, execute_git_sync
from .config import config

logger = logging.getLogger("Gravitas_ROUTER")

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
            docs = await container.memory.search(request.message, top_k=3)
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
    Purges existing memory first to ensure fresh data.
    """
    if not container.ingestor:
        return {"status": "error", "message": "Ingestor not initialized (Vector Store missing?)"}
    
    try:
        # 1. PURGE EXISTING DATA (Prevent staleness)
        if container.memory:
            logger.info("🧹 Purging old memory before re-scan...")
            await container.memory.purge()

        # 2. RUN INGESTION
        summary = await container.ingestor.ingest_all()
        
        if summary["status"] == "success":
            msg = f"Knowledge memory purged and re-ingested. Processed {summary['files_processed']} files ({summary['chunks_ingested']} chunks)."
            return {"status": "success", "message": msg, "summary": summary}
        else:
            return summary
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
    Server-Sent Events (SSE) stream for real-time health and telemetry metrics.
    """
    async def event_generator():
        from .database import db
        while True:
            # If client closes connection, stop sending
            if await request.is_disconnected():
                break

            # 1. Fetch Health Data (Reuse logic but faster)
            health_data = await get_detailed_health()
            
            # 2. Fetch Recent Stats (Optional: Add real-time tokens etc)
            # For now, just send health
            
            yield f"event: update\ndata: {json.dumps(health_data)}\n\n"
            
            await asyncio.sleep(2) # Stream every 2 seconds

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/system/reset")
async def reset_system():
    """
    Warms up the reset script to restore Gravitas to a clean state.
    """
    try:
        # Trigger the reset script in the background
        subprocess.Popen(["bash", "scripts/reset_gravitas.sh"])
        return {"status": "success", "message": "System reset sequence initiated. Containers will restart."}
    except Exception as e:
        logger.error(f"❌ RESET FAILURE: {e}")
        return {"status": "error", "message": str(e)}

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

logger = logging.getLogger("Gravitas_CONTAINER")

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
      - POSTGRES_HOST=Gravitas_postgres
      - QDRANT_HOST=Gravitas_qdrant
      - L1_URL=http://Gravitas_ollama:11434
      - L1_EMBED_URL=http://Gravitas_ollama_embed:11434
      - MINIO_HOST=Gravitas_minio
      # Ensure these match your .env
      - POSTGRES_USER=${DB_USER:-Gravitas_user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-Gravitas_pass}
      - POSTGRES_DB=${DB_NAME:-chat_history}
    ports:
      - "8001:8000" # Maps port 8000 inside to 8001 outside (just in case)
    depends_on:
      - Gravitas_postgres
      - qdrant
      - ollama
      - ollama_embed
    networks:
      - Gravitas_net
    restart: unless-stopped

  # --- GPU 0: GENERATION (TITAN RTX) ---
  ollama:
    image: ollama/ollama:latest
    container_name: Gravitas_ollama
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
      - Gravitas_net
    restart: always

  # --- GPU 1: EMBEDDINGS (GTX 1060) ---
  ollama_embed:
    image: ollama/ollama:latest
    container_name: Gravitas_ollama_embed
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
      - Gravitas_net
    restart: always

  # --- MEMORY: QDRANT (HYBRID VECTOR DB) ---
  qdrant:
    image: qdrant/qdrant:latest
    container_name: Gravitas_qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./data/qdrant:/qdrant/storage
    environment:
      - QDRANT_ALLOW_RECOVERY_MODE=true
    networks:
      - Gravitas_net
    restart: always

  # --- STORAGE: MINIO (OBJECT STORE) ---
  minio:
    image: minio/minio:latest
    container_name: Gravitas_minio
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
      - Gravitas_net
    restart: always

  # --- DATABASE: POSTGRES (HISTORY) ---
  Gravitas_postgres:
    image: postgres:16-alpine
    container_name: Gravitas_postgres
    environment:
      - POSTGRES_USER=${DB_USER:-Gravitas_user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-Gravitas_pass}
      - POSTGRES_DB=${DB_NAME:-chat_history}
    volumes:
      - ./data/postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - Gravitas_net
    restart: always

  # --- API: RAG BACKEND (LEGACY/ROUTER) ---
  rag_app:
    build: .
    container_name: Gravitas_rag_backend
    # Optional: If you run the main app via uvicorn
    command: uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload
    volumes:
      - .:/app
    ports:
      - "5050:5050"
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-Gravitas_user}:${DB_PASSWORD:-Gravitas_pass}@Gravitas_postgres:5432/${DB_NAME:-chat_history}
      - DB_HOST=Gravitas_postgres
      - L1_URL=http://Gravitas_ollama:11434
      - L1_EMBED_URL=http://Gravitas_ollama_embed:11434
    depends_on:
      - Gravitas_postgres
      - qdrant
    networks:
      - Gravitas_net

networks:
  Gravitas_net:
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
