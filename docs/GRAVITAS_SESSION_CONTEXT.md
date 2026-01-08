
# Gravitas Grounded Research - Session Context
**Generated:** 2026-01-08 13:43:25
**System:** Titan RTX (Local) + DeepInfra (Cloud)
**App State:** Docker Microservices


---
## HARDWARE OPERATIONS

*Missing docs/004_hardware_operations.md - Please create this file.*


---
## STRATEGIC ROADMAP

*Missing docs/ROADMAP.md - Please create this file.*


---
## PHYSICAL FILE MAP
```text
Gravitas/
    onArrival.txt
    .bashrc_gravitas
    task.md
    .gitignore
    rag_memory.db
    tmp.txt
    gravitas_mcp_config.json
    READ_ME_GRAVITAS_MASTER_MANUAL.md
    pyproject.toml
    docker-compose.yml
    Dockerfile.router
    requirements.txt
    .env
    PHASE_6_TODO.md
    PHASE_6_IMPLEMENTATION_SUMMARY.md
    Dockerfile.gatekeeper
    Dockerfile.guardian
    .dockerignore
    Dockerfile
    supervisor.log
    PHASE_7_TODO.md
    log_conf.yaml
    debug_rag_retrieval.py
    BACKUP_QUICKSTART.md
    CHANGELOG.md
    .env.example
        tools/
            switch_brain.py
        docs/
            README.md
            planning/
                ROADMAP.md
                rfcs/
                    Database_Decomposition_RFC-003.md
                    RFC-004_DYNAMIC_REGISTRY.md
                    Scaling_And_Migrations_RFC-005.md
                    Telemetry_Decoupling_RFC-002.md
            phases/
                Scaling_And_Migrations_Phase_2.md
                Phase_6/
                    TEST_AUDIT_PHASE6.md
                    TEST_AUDIT_PHASE6_FINAL.md
                    Phase_6_Value.md
                    todo/
                        Phase_6_TODO/
                            todo6.0Debt.md
                        Phase_6.5_TODO/
                            EXECUTION_SUMMARY.md
                            README.md
                            PROGRESS.md
                            QUICK_REFERENCE.md
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
                Phase_RFC001/
                    Phase1_Guardian_Extraction_Complete.md
                Phase_5/
                    PHASE_5_IMPLEMENTATION_REVIEW.md
                    PHASE_5_FINAL_COMPLETION_SUMMARY.md
                Phase_4.5/
                    PHASE_4_5_FINAL_VALIDATION_REPORT.md
                    PHASE_4.5_COMPLETION_SUMMARY.md
                Phase_7/
                    TODO7.md
            testing/
                TEST_GUIDE.md
                TEST_AUDIT_SUMMARY.md
                TEST_RESULTS_INTEGRATED_RAG.md
                SPECIFICATION_TESTING_SUMMARY.md
                TEST_AUDIT.md
                TELEMETRY_INTEGRATION_TEST_RESULTS.md
            rfcs/
                RFC-001-SupervisorDecomposition.md
                TEMPLATE.md
                CurrentDockerArchitectureAnalysis.md
                phases/
                    Supervisor_Decomposition_Complete_RFC-001.md
                    Database_Decomposition_Phase_1.md
                    Database_Decomposition_Strategy_RFC-003.md
                    Ghost_Shell_Architecture_Phase_6.5.md
                handovers/
                    handoff_to_gemini3_pro_2026-01-07.md
            sessions/
                SESSION_COMPLETE_SUMMARY.md
                COMPLETE_SESSION_SUMMARY.md
                SESSION_SUMMARY_RAG_TESTING.md
                Initial Context Prompt.md
            reference/
                gemini_3_model_guide.md
                function_cycles.md
                BACKUP_SETUP.md
                FAQ.md
                model_integration.md
            debug/
                RAG_DEBUG_ANALYSIS.md
                RESET_SCRIPT_UPDATE.md
                NEXUS_RESCAN_IMPROVEMENTS.md
                RAG_REFUSAL_RESOLUTION.md
            journals/
                Ollama_codellama_7b_dd97fe22-9e96-4aaf-a964-44548291c737.md
                Ollama_codellama_7b_journal.md
                Ollama_codellama_7b_bd7d8c0f-1714-4348-b3f7-ed7dcd19f76e.md
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232045.md
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232510.md
                ReasoningPipe_MockAgent_test_session_20260105_231220.md
                ReasoningPipe_ValidAgent_test_session_20260105_231731.md
                ReasoningPipe_Claude_Thinking_test_session_123.md
                PHASE_5_STRATEGIC_ASSESSMENT.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232117.md
                Ollama_codellama_7b_be1a7e14-a835-4761-a446-369adc96b2a3.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_231947.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232044.md
                Ollama_codellama_7b_3c12a719-d91d-4c30-ad95-7b7617e42a8c.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_deepinfra_789.md
                ReasoningPipe_Ollama_codellama_7b_test_ollama_456.md
                2026-01-04_executive.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232016.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232046.md
                ValidAgent_test_session_20260106_204312.md
                ValidAgent_journal.md
                ReasoningPipe_Claude_Thinking.md
                ReasoningPipe_ValidAgent_test_session_20260105_232505.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232045.md
                Ollama_codellama_7b_e1a0e848-85b0-4492-85ba-b55507ae5c3f.md
                ReasoningPipe_ValidAgent.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232117.md
                current_session.md
                2026-01-04_Strategy_Session.md
                2026-01-07_thoughts.md
                ReasoningPipe_Ollama_codellama_7b.md
                2026-01-05_thoughts.md
                2026-01-07_executive.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_231946.md
                2026-01-05_executive.md
                Ollama_codellama_7b_d17edc15-7b51-4484-8620-45dc2d1b5535.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder.md
                Ollama_codellama_7b_a8206e0b-6e45-47aa-831b-224875b0b6f3.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232510.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232017.md
                ReasoningPipe_MockAgent.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232510.md
                ReasoningPipe_Gemini_Thinking_test_session_20260105_232117.md
                ReasoningPipe_Ollama_model-for-testing_test_session_20260105_232117.md
                ReasoningPipe_Gemini_Thinking.md
                Ollama_codellama_7b_3f2d0e28-2d24-44e7-bf42-45da42148175.md
                ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_session_20260105_232511.md
                ReasoningPipe_Claude_Thinking_test_session_20260105_232016.md
                Ollama_codellama_7b_98088501-5df0-49e6-9479-69d3adf84e1b.md
                ReasoningPipe_Ollama_model-for-testing.md
                Ollama_codellama_7b_b0db77d6-3526-4225-8afa-d770f2a0e4a1.md
                2026-01-04_thoughts.md
            archived/
                COMPLETED_PHASES_1-5.md
                ROADMAP_COMPLETION_CRITERIA_UPDATE.md
                todo9.md
                completed_phase9.md
                ROADMAP_ENTERPRISE_draft.md
                developerNotes.md
            concepts/
                002_intuition_and_logic.md
                006_the_user_experience.md
                005_infrastructure_and_vaults.md
                001_enterprise_agent_taxonomy.md
                004_identity_and_engine.md
                003_cognitive_tiers.md
            architecture/
                001_core_architecture.md
                009_access_control.md
                003_security_gatekeeper.md
                008_reasoning_pipes.md
                thinking_transparency.md
                004_hardware_operations.md
                GRAVITAS_NOMENCLATURE.md
                002_vector_memory.md
                000_MASTER_OVERVIEW.md
                007_model_governance.md
            development/
                hardware_rig.md
                WRAPPER_DEVELOPMENT_GUIDE.md
                006_TELEMETRY_CALIBRATION.md
                CODING_STANDARDS.md
                GOOGLE_ANTIGRAVITY_SPEC.md
                HOWTO_DEV_REMINDERS.md
                005_development_protocols.md
                TESTING_GUIDE.md
            incidents/
                INCIDENT_LOG.md
                criticalSupervisorFailureReport.md
                todoSupervisorDebugV2.md
                2026-01-08_dependency_failures.md
                archived/
                    INCIDENT_LOG_2026-01-07.md
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
            __init__.py
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
            tools/
                __init__.py
                engineer/
                    __init__.py
                    log_entry.py
                    inventory.sh
                    debug_import.py
                    global_rename.py
                    reset_gravitas.sh
                    mcp_entrypoint.sh
                    audit_gravitas.sh
                    monitor.sh
                    debug_network.py
                    manager.py
                librarian/
                    __init__.py
                    generate_context.py
                    load_knowledge.py
                    manual_ingest.py
                    ingestor.py
                    sync_external_context.py
                    init_db.sql
                    migrations/
                        001_add_identity_columns.sql
                accountant/
                    __init__.py
                    usage_stats.py
                supervisor/
                    __init__.py
                    model_inventory.py
                    warmup.py
                    check_models.py
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
                Supervisor_Managed_Agent.json
            governance/
                inspector.py
                global_renamer.py
                accountant.py
            config/
                __init__.py
                access_policies.yaml
            services/
                __init__.py
                audit/
                    shadow_audit.py
                scheduler/
                    lock.py
                    queue.py
                guardian/
                    __init__.py
                    main.py
                    alembic.ini
                    core.py
                    database.py
                    migrations/
                        env.py
                        README
                        script.py.mako
                        versions/
                            baaed4835b03_initial_schema.py
                router/
                    guardian_client.py
                    main.py
                    alembic.ini
                    api.py
                    database.py
                    gatekeeper_client.py
                    wrappers/
                        __init__.py
                        base_wrapper.py
                        deepinfra_wrapper.py
                        ollama_wrapper.py
                        claude_wrapper.py
                        gemini_wrapper.py
                    migrations/
                        env.py
                        README
                        script.py.mako
                        versions/
                            35f8d079f4de_initial_schema.py
                registry/
                    __init__.py
                    ghost_registry.py
                    agent_registry.py
                    shell_registry.py
                dispatcher/
                    router.py
                security/
                    __init__.py
                    badges.py
                    deps.py
                    policy_engine.py
                    auth.py
                    audit_log.py
                gatekeeper/
                    main.py
                    alembic.ini
                    policy.py
                    database.py
                    audit.py
                    auth.py
                    migrations/
                        env.py
                        README
                        script.py.mako
                        versions/
                            c6b1b8a06e4c_initial_schema.py
                supervisor/
                    __init__.py
                    auditor.py
                    guardian_client.py
                    main.py
                    guardian.py
                    gatekeeper_client.py
                    router.py
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
                AntigravitySupport.md
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
                test_supervisor_router.py
                test_repo_walker.py
                test_claude_wrapper.py
                test_queue_basic.py
            integration/
                test_reasoning_pipe_e2e.py
                test_audit_buffering.py
                test_gatekeeper.py
                test_phase5_model_governance.py
                test_router_extraction.py
                test_phase7_security.py
            scripts/
                verify_repo_walker.py
                verify_chat.py
                test_minio.py
                test_connections.py
                verify_phase5.py
                titan_stress.py
                verify_gpu_distribution.py
                test_qwen3_connection.py
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
            setup_backup.sh
            log_entry.py
            generate_context.py
            reset_wrapper.sh
            backup_now.sh
            warmup.py
            restore_backup.sh
            list_backups.ps1
            reset_gravitas.sh
            backup_now.ps1
            restore_backup.ps1
            list_backups.sh
        .pytest_cache/
            .gitignore
            README.md
            CACHEDIR.TAG
            v/
                cache/
                    lastfailed
                    nodeids
                    stepwise
        requirements/
            router.txt
            guardian.txt
            gatekeeper.txt
            common.txt
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
*Not Found*

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
      - L1_URL=http://gravitas_router:8004
      - L1_EMBED_URL=http://Gravitas_ollama_embed:11434
      - MINIO_HOST=Gravitas_minio
      # Ensure these match your .env
      - POSTGRES_USER=${DB_USER:-Gravitas_user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-Gravitas_pass}
      - POSTGRES_DB=${DB_NAME:-chat_history}
    ports:
      - "8001:8000" # Maps port 8000 inside to 8001 outside (just in case)
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

  # --- API: GRAVITAS LOBBY (PUBLIC ENTRY POINT) ---
  gravitas_lobby:
    build: .
    container_name: Gravitas_lobby_v2
    # Optional: If you run the main app via uvicorn
    command: uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload
    volumes:
      - .:/app
    ports:
      - "5050:5050"
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-Gravitas_user}:${DB_PASSWORD:-Gravitas_pass}@Gravitas_postgres:5432/${DB_NAME:-chat_history}
      - DB_HOST=Gravitas_postgres
      - L1_URL=http://gravitas_router:8004
      - L1_EMBED_URL=http://Gravitas_ollama_embed:11434
    networks:
      - Gravitas_net
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [ gpu ]

  gravitas_gatekeeper:
    build:
      context: .
      dockerfile: Dockerfile.gatekeeper
    container_name: gravitas_gatekeeper
    ports:
      - "8002:8001"
    environment:
      - DATABASE_URL=postgresql://Gravitas_user:Gravitas_pass@Gravitas_postgres:5432/chat_history
      - DB_HOST=Gravitas_postgres
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-jwt-secret-key-change-me}
      - ACCESS_POLICY_PATH=app/config/access_policies.yaml
    depends_on:
      - Gravitas_postgres
    networks:
      - Gravitas_net

  gravitas_guardian:
    build:
      context: .
      dockerfile: Dockerfile.guardian
    container_name: gravitas_guardian
    command: uvicorn app.services.guardian.main:app --host 0.0.0.0 --port 8003
    ports:
      - "8003:8003"
    volumes:
      - ./app/.certificates:/app/app/.certificates:ro # Read-only certificate mount
    environment:
      - CERTIFICATES_DIR=/app/app/.certificates
    networks:
      - Gravitas_net
    restart: unless-stopped

  gravitas_router:
    build:
      context: .
      dockerfile: Dockerfile.router
    container_name: gravitas_router
    ports:
      - "8005:8004"
    environment:
      - OLLAMA_URL=http://Gravitas_ollama:11434/v1/chat/completions
      - GATEKEEPER_URL=http://gravitas_gatekeeper:8001
      - GUARDIAN_URL=http://gravitas_guardian:8003
      - AUTH_DISABLED=false
      # Add provider keys if needed, e.g. GEMINI_API_KEY from .env
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DEEPINFRA_API_KEY=${DEEPINFRA_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - gravitas_gatekeeper
      - gravitas_guardian
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
*Not Found*
