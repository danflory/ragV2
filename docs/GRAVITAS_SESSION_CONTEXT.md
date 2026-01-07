
# Gravitas Grounded Research - Session Context
**Generated:** 2026-01-06 07:16:37
**System:** Titan RTX (Local) + DeepInfra (Cloud)
**App State:** Docker Microservices


---
## HARDWARE OPERATIONS

# 004_HARDWARE_OPERATIONS.md
# STATUS: ACTIVE
# VERSION: 5.0.0 (Model Governance)

## 1. DUAL-GPU ARCHITECTURE
The system leverages **dual NVIDIA GPUs** for parallel processing and optimal resource utilization.

*   **GPU 0 (Titan RTX 24GB):** Primary Compute / Generation
    * **Role:** Dedicated AI Inference / Local LLM (L1) / Training
    * **Services:** `Gravitas_ollama` (Port 11434)
    * **Models:** `gemma2:27b-instruct-q4_k_m` (~17GB VRAM)
    * **Routing:** Managed by `gravitas_supervisor` for intelligent tier selection

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
5.  **Intelligent Routing:** Supervisor service monitors VRAM and routes to L2/L3 when local resources constrained (see `007_model_governance.md`).

## 3. MICROSERVICES TOPOLOGY
The system runs in a multi-container environment with dedicated services:

*   **`gravitas_supervisor`:** Intelligent routing proxy for L1/L2/L3 tier selection (Port 8000)
*   **`Gravitas_mcp`:** Main application container with sleep infinity for manual process injection
*   **`Gravitas_ollama`:** L1 model hosting (GPU 0 - Titan RTX)
*   **`Gravitas_ollama_embed`:** Embedding models (GPU 1 - GTX 1060)
*   **`Gravitas_qdrant`:** Hybrid vector database (CPU)
*   **`Gravitas_minio`:** Object storage for raw documents (CPU)
*   **`Gravitas_postgres`:** Chat history, telemetry logging, and routing audit (CPU)
*   **`Gravitas_rag_backend`:** Legacy RAG API service (Port 5050)

## 4. ADVANCED HARDWARE FEATURES
* **Parallel Processing:** Embeddings don't block generation
* **VRAM Optimization:** Frees 6-7GB on Titan RTX for larger context
* **Cost Efficiency:** GTX 1060 runs productive workloads instead of idle display duty
* **Circuit Breaker:** GPU embedding with CPU fallback for resilience
* **Intelligent Offloading:** Automatic L2/L3 routing when local GPUs saturated (Phase 5)


---
## STRATEGIC ROADMAP

# GRAVITAS GROUNDED RESEARCH - STRATEGIC ROADMAP

## CURRENT STATE: v5.0.0 (DYNAMIC GOVERNANCE)
The core infrastructure is stable. Phase 5 (Model Governance) is complete, providing a standalone supervisor service, agent registry, and priority-aware routing. Phase 6 (Reasoning Pipes) is currently in early implementation.

---

## PHASE COMPLETION CRITERIA

**A phase is NOT considered complete until ALL of the following requirements are met:**

### 1. Documentation Requirements
- [x] All relevant `docs/00x_*.md` specifications updated
- [x] Specification version numbers incremented
- [x] `ROADMAP.md` updated with phase details
- [x] Phase completion summary document created

### 2. Test Suite Requirements
- [x] Specification test files created (`test_spec_00X_*.py`)
- [x] Integration test files created for new features
- [x] All unit tests passing locally
- [x] Test runner executes successfully (`python tests/run_spec_tests.py`)

### 3. Docker Integration Requirements
- [x] All Docker containers configured in `docker-compose.yml`
- [x] Integration tests pass inside Docker environment
- [x] **Full reset test passes:** `bash scripts/reset_gravitas.sh` followed by tests
- [x] Service health checks confirm all containers running
- [x] Database persistence verified

### 4. Production Readiness
- [x] No failing tests in test suite
- [x] No Docker container failures
- [x] Performance benchmarks met
- [x] Documentation complete and accurate

---

## COMPLETED PHASES

### PHASE 1: THE FOUNDATION (QDRANT & MINIO)
- [x] **Hybrid Storage:** Split vectors (Qdrant) from blobs (MinIO) for hardware efficiency.
- [x] **Verification:** Full ingestion and search pipeline verified in `tests/`.

### PHASE 2: PERSISTENCE & TELEMETRY
- [x] **Infrastructure:** Provisioned `Gravitas_postgres` for chat history and metrics.
- [x] **Telemetry:** Implemented `app/telemetry.py` for VRAM tracking and system events.

### PHASE 3: THE GRAVITAS EVOLUTION (REBRANDING)
- [x] **Consistency:** Global rename of all legacy terms to **Gravitas**.
- [x] **Automation:** Hooked session context generation into the system startup.
- [x] **Protocols:** Established `docs/GRAVITAS_NOMENCLATURE.md` and `docs/005_development_protocols.md`.

### PHASE 4: COMMAND & CONTROL (THE NEXUS DASHBOARD)
- [x] **Master Control Dashboard:** Unified Web UI for service management, model pulling, and system resets.
- [x] **Real-time Metrics:** Integrated VRAM and Docker health metrics via SSE.
- [x] **Health API:** Implemented `/health` endpoints for all containers.

### PHASE 4.5: GRANULAR TELEMETRY CALIBRATION (THE SENSORS)
- [x] **Sensor Implementation:** Upgraded `app/telemetry.py` for Load and Thought latency tracking.
- [x] **Weighted Aggregation:** Refactored logging to measure Work Units (Tokens) and Efficiency Scores.
- [x] **Retention Policy:** Established a 60-day historic window in Postgres.
- [x] **Footprint Monitor:** Added dashboard widget for telemetry disk usage.
- [x] **Auto-Pruning:** Implemented the 60-day pruning mechanism.

**Verification (2026-01-05):**
- [x] **Documentation:** `006_TELEMETRY_CALIBRATION.md` created
- [x] **Integration:** `test_docker_telemetry_integration.py` - **3/3 PASSED**
- [x] **Efficiency:** 15.01 ms/token performance verified.

### PHASE 5: DYNAMIC MODEL GOVERNANCE (THE SUPERVISOR)
- [x] **Standalone Supervisor:** Built `gravitas_supervisor` Docker proxy service for L1/L2/L3 tiers.
- [x] **Agent Registry:** Defined agent capabilities, costs, and performance metrics in code.
- [x] **L1 Orbit Logic:** Implemented Request Queuing, Model Locking, and Context Persistence.
- [x] **Priority Yield:** Added "Mr. Big Guy" logic for high-priority task preemption.
- [x] **Data-Driven Dispatcher:** Heuristic routing based on complexity and Phase 4.5 telemetry.
- [x] **Shadow-Audit Loop:** passive self-correction mechanism logging dispatch decisions.

**Verification (2026-01-05):**
- [x] **Documentation:** `007_model_governance.md` created (v5.0.0)
- [x] **Integration:** `test_phase5_model_governance.py` - **6/6 PASSED**
- [x] **Core Services:** RequestQueue, ModelLock, DispatcherRouter, AgentRegistry, ShadowAudit operational.

## ACTIVE PHASE (COMPLETED)

### PHASE 6: SELF-LEARNING DATA (REASONING PIPES)
**Target**: Enable wrapper-certified reasoning capture for L1, L2, and L3 models.

**Architecture: Wrapper Certification Model**
- Supervisor validates agent code (not data).
- Agents are responsible for parsing and pipe writing.
- **Benefits**: Scalability, lower latency, distributed parsing.

#### 1. Core Infrastructure
- [x] **ReasoningPipe Library**: Implement `app/lib/reasoning_pipe.py` (log_thought, log_action, finalize).
- [x] **Supervisor Guardian**: Implement `app/services/supervisor/guardian.py` for runtime enforcement.
- [x] **Markdown Protocol**: Standardized `ReasoningPipe_{agent}_{session}.md` format.

#### 2. Certification System
- [x] **Wrapper Certifier**: Static analysis and dynamic validation of agent wrappers.
- [x] **Certificate Issuance**: SHA-256 signed certs with 30-day validity.
- [x] **Compliance Auditor**: Monthly quality scoring and re-certification triggers.

#### 3. Agent Wrapper Implementations
- [x] **L3 Frontier**: Gemini 2.0 Flash Thinking & Claude 4.5 Sonnet Thinking.
- [x] **L2 Specialized**: DeepInfra (Qwen2.5-Coder).
- [x] **L1 Local**: Ollama base wrapper (codellama, llama3, etc.).

#### 4. Testing & Validation
- [x] **Specification Tests**: 100% coverage for `reasoning_pipe.py` and Guardian.
- [x] **Certification Workflow**: End-to-end test of the certification process.
- [x] **Performance Audit**: Ensure < 5% overhead from reasoning capture.

#### 5. Documentation
- [x] **Wrapper Guide**: `docs/WRAPPER_DEVELOPMENT_GUIDE.md` created.
- [x] **Governance**: `docs/007_model_governance.md` updated with certification routing.

**Verification Checklist:**
- [x] All 4 initial wrappers certified (`python certifier.py --list`).
- [x] Integration tests pass in Docker environment.
- [x] Reasoning documentation updated to v6.0.0.

---

## UPCOMING PHASES

### PHASE 7: THEOLOGY ENGINE (KNOWLEDGE GRAPH)
- [ ] **Infrastructure:** Deploy **Neo4j** (Graph DB) alongside Qdrant (Vector DB).
- [ ] **The Librarian:** Implement the `GravitasLibrarian` agent responsible for knowledge ingestion and retrieval.
- [ ] **Entity Extraction Pipeline:** Build the "Ingestion Engine" to parse books, extract theological concepts, and link them (Graph-ETL).
- [ ] **GraphRAG:** Implement Graph-Augmented Retrieval to answer complex, multi-hop theological queries.
- [ ] **Orchestration:** Update Supervisor to route "Knowledge Queries" to the Librarian.

### PHASE 8: THE AGENTIC ENTERPRISE (SPECIALIZATION)
- [ ] **Agent Registry 2.0:** Formalize "Job Descriptions" for all agents (Librarian, Scout, Theologian, Engineer).
- [ ] **Cloud Bursting:** Implement Supervisor logic to overflow heavy reasoning tasks to L3 Cloud Agents (e.g., DeepInfra/Gemini).
- [ ] **The Scout:** Implement `GravitasScout` for live web probing and external research.
- [ ] **Iterative Reasoning:** Formalize "Scout-to-Theologian" feedback loops for deep research tasks.

### PHASE 9: GRAVITAS AGENTIC INFRASTRUCTURE
- [ ] **Mirroring Protocols:** Standardized `.gravitas_agent` directory structures.
- [ ] **Recon Protocol:** Generalized startup sequence for all agents to sync with project state.
- [ ] **Verification:** Dockerized execution of standardized agent startup.

### PHASE 10: INTELLIGENCE AUDIT & BENCHMARKING
- [ ] **Bi-Weekly Pulse:** Automated sweep of Ollama/DeepInfra/Google for new releases.
- [ ] **Independent Benchmarking:** Project-specific RAG/Coding performance scoring.
- [ ] **Automation:** Automated promotion/demotion logic based on scores.

---

## BACKLOG / TECH DEBT
- [ ] **Secret Hygiene:** Scan codebase for hardcoded keys.
- [x] **Journal Rotation:** Implement dated journal snapshots. (Done: `docs/journals/`)
- [ ] **VENV Hardening:** Standardize cross-platform dependency resolution.
- [ ] **Error Boundary:** Improve global exception handling for high-latency storage operations.


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
    PHASE_6_TODO.md
    PHASE_6_IMPLEMENTATION_SUMMARY.md
    .dockerignore
    Dockerfile
    PHASE_7_TODO.md
    log_conf.yaml
    debug_rag_retrieval.py
    CHANGELOG.md
    .env.example
        tools/
            switch_brain.py
        docs/
            TEST_GUIDE.md
            PHASE_4_5_FINAL_VALIDATION_REPORT.md
            PHASE_5_IMPLEMENTATION_REVIEW.md
            hardware_rig.md
            PHASE_5_FINAL_COMPLETION_SUMMARY.md
            gemini_3_model_guide.md
            RAG_DEBUG_ANALYSIS.md
            WRAPPER_DEVELOPMENT_GUIDE.md
            006_TELEMETRY_CALIBRATION.md
            001_core_architecture.md
            STRATEGY_SESSION_2026_01_04.md
            RESET_SCRIPT_UPDATE.md
            ROADMAP_COMPLETION_CRITERIA_UPDATE.md
            003_security_gatekeeper.md
            GOOGLE_ANTIGRAVITY_SPEC.md
            HOWTO_DEV_REMINDERS.md
            SESSION_COMPLETE_SUMMARY.md
            function_cycles.md
            008_reasoning_pipes.md
            COMPLETE_SESSION_SUMMARY.md
            TEST_RESULTS_INTEGRATED_RAG.md
            NEXUS_RESCAN_IMPROVEMENTS.md
            SPECIFICATION_TESTING_SUMMARY.md
            TEST_AUDIT.md
            SESSION_SUMMARY_RAG_TESTING.md
            PHASE_4.5_COMPLETION_SUMMARY.md
            ROADMAP.md
            developerNotes.md
            005_development_protocols.md
            004_hardware_operations.md
            GRAVITAS_NOMENCLATURE.md
            TELEMETRY_INTEGRATION_TEST_RESULTS.md
            002_vector_memory.md
            FAQ.md
            model_integration.md
            000_MASTER_OVERVIEW.md
            Phase_6_Value.md
            Initial Context Prompt.md
            007_model_governance.md
            RAG_REFUSAL_RESOLUTION.md
            Phase_6TODO/
                Priority_2_Wrappers.md
                Task_5_2_Update_Existing_Specs.md
                Priority_3_Certification_System.md
                Task_2_4_DeepInfra_Wrapper.md
                README.md
                Task_2_2_Claude_Sonnet_4_5_Thinking_Wrapper.md
                Task_4_1_Specification_Tests.md
                Task_1_1_ReasoningPipe_Standard_Library.md
                Task_4_2_Wrapper_Certification_Tests.md
                Priority_4_Testing.md
                Task_1_2_Supervisor_Guardian.md
                Task_1_3_Base_Wrapper_Class.md
                Task_3_2_Monthly_Auditor.md
                Task_2_3_Ollama_Local_Models_Wrapper.md
                Priority_1_Infrastructure.md
                Task_2_1_Gemini_2_0_Flash_Thinking_Wrapper.md
                Task_4_3_End_to_End_Integration_Tests.md
                Task_5_1_Wrapper_Development_Guide.md
                Task_3_1_Wrapper_Certifier.md
                Priority_5_Documentation.md
            journals/
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232045.md
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232510.md
                ReasoningPipe_MockAgent_test_session_20260105_231220.md
                ReasoningPipe_ValidAgent_test_session_20260105_231731.md
                ReasoningPipe_Claude_Thinking_test_session_123.md
                PHASE_5_STRATEGIC_ASSESSMENT.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232117.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_231947.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232044.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_deepinfra_789.md
                ReasoningPipe_Ollama_codellama_7b_test_ollama_456.md
                2026-01-04_executive.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232016.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232046.md
                ReasoningPipe_Claude_Thinking.md
                ReasoningPipe_ValidAgent_test_session_20260105_232505.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232045.md
                ReasoningPipe_ValidAgent.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232117.md
                current_session.md
                ReasoningPipe_Ollama_codellama_7b.md
                2026-01-05_thoughts.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_231946.md
                2026-01-05_executive.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232510.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232017.md
                ReasoningPipe_MockAgent.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232510.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232117.md
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232117.md
                ReasoningPipe_Gemini_Thinking.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232511.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232016.md
                ReasoningPipe_Ollama_model-for-testing.md
                2026-01-04_thoughts.md
            archived/
                todo9.md
                completed_phase9.md
            architecture/
                thinking_transparency.md
        gravitas_supervisor/
            main.py
            Dockerfile
            clients/
                deepinfra.py
                gemini.py
            services/
                scheduler/
                    lock.py
                    queue.py
                dispatcher/
                    router.py
            utils/
                repo_walker.py
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
            lib/
                __init__.py
                reasoning_pipe.py
            clients/
                deepinfra.py
                gemini.py
            agents/
                librarian.py
                scout.py
            wrappers/
                __init__.py
                base_wrapper.py
                deepinfra_wrapper.py
                ollama_wrapper.py
                claude_wrapper.py
                gemini_wrapper.py
            .certificates/
                DeepInfra_Qwen2.5-Coder.json
                Claude_Thinking.json
                Ollama_codellama_7b.json
                MockAgent.json
            governance/
                inspector.py
                global_renamer.py
                accountant.py
            services/
                audit/
                    shadow_audit.py
                scheduler/
                    lock.py
                    queue.py
                registry/
                    agent_registry.py
                dispatcher/
                    router.py
                supervisor/
                    __init__.py
                    auditor.py
                    guardian.py
                    certifier.py
            utils/
                repo_walker.py
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
            VERSION_POLICY.md
        tests/
            test_rag_diagnostics.py
            test_integration_telemetry_phase45.py
            test_docker_telemetry_integration.py
            test_mode_switching.py
            test_minio_storage.py
            test_L3_google.py
            test_l3_integration.py
            test_integrated_rag_prompts.py
            test_vram_safety.py
            test_ingestion_pipeline.py
            test_spec_005_development_protocols.py
            test_protocol_e2e.py
            test_spec_003_security_gatekeeper.py
            test_L2_connection.py
            test_embed_breaker.py
            README.md
            test_safety_logic.py
            test_telemetry_standalone_integration.py
            test_telemetry.py
            test_hybrid_search.py
            test_inspector.py
            test_mcp_connection.py
            test_advanced_rag.py
            test_dual_gpu.py
            test_wrapper_certification.py
            test_spec_002_vector_memory.py
            test_ioc_refactor.py
            test_spec_001_core_architecture.py
            test_infra_connection.py
            test_3L_pipeline.py
            test_ioc_baseline.py
            test_warm_librarian.py
            test_deepseek_sidecar.py
            test_spec_006_telemetry_calibration.py
            test_nexus_api.py
            test_librarian.py
            test_memory_logic.py
            test_accountant.py
            test_spec_004_hardware_operations.py
            test_memory_pruning.py
            test_reflex.py
            test_current_stack.py
            test_spec_008_reasoning_pipes.py
            run_spec_tests.py
            unit/
                test_model_lock.py
                test_supervisor_guardian.py
                test_dispatcher_router.py
                test_queue_logic.py
                test_clients.py
                test_base_wrapper.py
                test_gemini_wrapper.py
                test_reasoning_pipe.py
                test_repo_walker.py
                test_queue_basic.py
            integration/
                test_reasoning_pipe_e2e.py
                test_phase5_model_governance.py
            manual/
                test_deepinfra_wrapper_mock.py
                test_ollama_wrapper_mock.py
                test_claude_wrapper_mock.py
        .vscode/
            sessions.json
            settings.json
        ANTIGRAVITY_Scripts/
            maintenance.py
            reasoning_pipe.py
        scripts/
            verify_repo_walker.py
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
            test_connections.py
            verify_phase5.py
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
        self.timeout = 180.0

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
    Restricted to RAG mode only.
    """
    if container.current_mode != config.MODE_RAG:
        return {"status": "error", "message": "Ingestion is restricted to RAG mode."}

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

@router.get("/telemetry/footprint")
async def get_telemetry_footprint():
    """
    Returns telemetry database footprint metrics for monitoring.
    """
    try:
        from .telemetry import telemetry
        footprint = await telemetry.get_telemetry_footprint()
        
        if footprint:
            return {"status": "success", "footprint": footprint}
        else:
            return {"status": "error", "message": "Failed to retrieve telemetry footprint"}
    except Exception as e:
        logger.error(f"❌ TELEMETRY FOOTPRINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/telemetry/60day")
async def get_60day_telemetry():
    """
    Returns 60-day historic telemetry statistics for performance analysis.
    """
    try:
        from .telemetry import telemetry
        stats = await telemetry.get_60day_statistics()
        
        if stats:
            return {"status": "success", "statistics": stats}
        else:
            return {"status": "error", "message": "Failed to retrieve 60-day statistics"}
    except Exception as e:
        logger.error(f"❌ 60-DAY TELEMETRY ERROR: {e}")
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
    Manually triggers the Librarian Agent to process docs/ and app/.
    Restricted to RAG mode only.
    """
    if container.current_mode != config.MODE_RAG:
        return {"status": "error", "message": "Librarian is restricted to RAG mode."}

    try:
        result = await container.librarian.process_docs()
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
      - L1_URL=http://gravitas_supervisor:8000
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
      - L1_URL=http://gravitas_supervisor:8000
      - L1_EMBED_URL=http://Gravitas_ollama_embed:11434
    depends_on:
      - Gravitas_postgres
      - qdrant
      - gravitas_supervisor
    networks:
      - Gravitas_net
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [ gpu ]

  # --- SUPERVISOR: DISPATCH AND QUEUE ---
  gravitas_supervisor:
    build:
      context: ./gravitas_supervisor
    container_name: gravitas_supervisor
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://Gravitas_ollama:11434/v1/chat/completions
    depends_on:
      - ollama
    networks:
      - Gravitas_net
    restart: unless-stopped

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
