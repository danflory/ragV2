# GRAVITAS GROUNDED RESEARCH - STRATEGIC ROADMAP

## CURRENT STATE: v4.5.0 (COMMAND & CONTROL)
The core infrastructure (Dockerized local RAG, Dual-GPU orchestration, Qdrant Memory + MinIO Storage, Postgres History) is stable. Agentic construction via Antigravity is active. The Nexus Dashboard with real-time VRAM monitoring and service management is now operational.

---

## PHASE COMPLETION CRITERIA

**A phase is NOT considered complete until ALL of the following requirements are met:**

### 1. Documentation Requirements ✅
- [ ] All relevant `docs/00x_*.md` specifications updated to reflect phase implementation
- [ ] Specification version numbers incremented
- [ ] `ROADMAP.md` updated with phase details
- [ ] Phase completion summary document created

### 2. Test Suite Requirements ✅
- [ ] Specification test files created (`test_spec_00X_*.py`)
- [ ] Integration test files created for new features
- [ ] All unit tests passing locally
- [ ] Test runner executes successfully (`python tests/run_spec_tests.py`)

### 3. Docker Integration Requirements ✅
- [ ] All Docker containers configured in `docker-compose.yml`
- [ ] Integration tests pass inside Docker environment
- [ ] **Full reset test passes:** `bash scripts/reset_gravitas.sh` followed by Docker integration tests
- [ ] Service health checks confirm all containers running
- [ ] Database persistence verified

### 4. Production Readiness ✅
- [ ] No failing tests in test suite
- [ ] No Docker container failures
- [ ] Performance benchmarks met (if applicable)
- [ ] Documentation complete and accurate

**Example Phase 4.5 Completion Verification:**
```bash
# 1. Reset all services
bash scripts/reset_gravitas.sh

# 2. Run integration tests in Docker
docker exec gravitas_mcp python /app/tests/test_docker_telemetry_integration.py

# 3. Run specification tests
python tests/run_spec_tests.py

# Result: ALL tests must pass (100%) before phase is marked complete
```

---

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

### PHASE 4: COMMAND & CONTROL (THE NEXUS DASHBOARD)
* [x] **Master Control Dashboard:** Unified Web UI for service management, model pulling, and system resets. **Includes integrated VRAM and Docker health metrics via Server-Sent Events (SSE)** for real-time monitoring.
* [x] **Health API:** Implement `/health` endpoints for all containers to feed real-time status to the Nexus.

### PHASE 4.5: GRANULAR TELEMETRY CALIBRATION (THE SENSORS)
* [x] **Sensor Implementation:** Upgrade `app/telemetry.py` to record sub-second metrics: **Load Latency** (VRAM setup) and **Thought Latency** (Inference Speed).
* [x] **Weighted Telemetry Aggregation:** 
    * **Pre-Calculation**: Refactor logging logic to measure "Work Units" (Tokens Generated) *before* database entry.
    * **The Efficiency Score**: Store **Latency-Per-Token** (Weighted) rather than flat temporal averages to accurately reflected system strain under load.
* [x] **The 60-Day Historic Window:** Establish a 60-day data retention policy in Postgres to track long-term hardware performance.
* [x] **Safety (Aggregation & Monitoring):** 
    * **Aggregation**: Average the Weighted Efficiency Scores every 60s to prevent database bloat.
    * **Dashboard Widget**: Create a "Telemetry Footprint" monitor to track disk space used by the millions of potential hits.
    * **Auto-Pruning Logic**: Implement the 60-day pruning mechanism in `ANTIGRAVITY_Scripts/maintenance.py` (Deferred from initial setup, now placed here).

**Phase 4.5 Completion Verification (2026-01-05):**
- [x] **Documentation:** `006_TELEMETRY_CALIBRATION.md` created (v4.5.0)
- [x] **Specs Updated:** All 00x specs updated to v4.5.0
- [x] **Test Suite:** `test_spec_006_telemetry_calibration.py` created (9 test classes)
- [x] **Integration Tests:** `test_docker_telemetry_integration.py` - **3/3 PASSED** ✅
- [x] **Reset Verification:** Docker tests pass after `reset_gravitas.sh`
- [x] **Docker Health:** All services running (postgres, qdrant, minio, ollama)
- [x] **Performance:** Sub-second precision verified (0.48μs), 15.01 ms/token efficiency
- [x] **Summary:** `PHASE_4.5_FINAL_VALIDATION_REPORT.md` created

### PHASE 5: DYNAMIC MODEL GOVERNANCE (THE SUPERVISOR)
* [x] **Infrastructure (Supervisor Service):** Build `gravitas_supervisor` as a standalone Docker proxy service. It acts as the traffic interceptor for three tiers:
    * **L1 (Local):** Zero-cost, privacy-first (Ollama).
    * **L2 (Specialized Cloud):** Low-cost, high-speed specialized agents (DeepInfra).
    * **L3 (Frontier Intelligence):** High-cost, maximum reasoning (Gemini 1.5 Pro).
* [x] **Agent Registry:** Define the "Gravitas Enterprise of Agents" in code, mapping capabilities, costs, and standardized performance metrics to specific models.
* [x] **L1 Orbit Logic (Queuing & Preemption):** 
    * **Context Persistence:** If Model A is loaded and has a queue, incoming requests for Model B are buffered to prevent "Context Thrashing" (rapid load/unload cycles).
    * **Disruption Management:** "Delay is acceptable; Disruption is not."
    * **Priority Yield (Mr. Big Guy):** Implement logic where a sufficiently high-priority task forces a running queue to yield.
* [x] **Data-Driven Dispatcher:** Implement a "Heuristic + Telemetry" routing algorithm. Complexity estimation routes to the appropriate Tier (L1/L2/L3), while Telemetry (Phase 4.5 data) determines specific model selection within that tier.
* [x] **Shadow-Audit Loop:** A passive "Self-Correction" mechanism that logs every dispatch decision (Expected vs. Actual performance) to build a dataset for future autonomous adjustment.

**Phase 5 Completion Verification (2026-01-05):**
- [x] **Documentation**: `007_model_governance.md` created (v5.0.0)
- [x] **Specs Updated:** `004_hardware_operations.md` updated to v5.0.0
- [x] **Core Components:** RequestQueue, ModelLock, DispatcherRouter, AgentRegistry, ShadowAuditLoop, DeepInfraClient, GeminiClient, repo_walker
- [x] **Integration Tests:** `test_phase5_model_governance.py` - **6/6 PASSED** ✅
- [x] **Unit Tests:** Component tests - **5/5 PASSED** ✅
- [x] **Docker Integration:** `gravitas_supervisor` service operational (port 8000)
- [x] **Summary:** `PHASE_5_IMPLEMENTATION_REVIEW.md` created

---

## UPCOMING PHASES

**Note:** Each phase below requires completion verification (see criteria above) before being marked as done.

### PHASE 6: SELF-LEARNING DATA (REASONING PIPES)

**Architecture Decision (RESOLVED):**
> **Wrapper Certification Model:** The Supervisor validates agent wrapper code (not token streams). Each agent is self-contained and responsible for:
> 1. Parsing model-specific reasoning output
> 2. Writing ReasoningPipe files in standardized format
> 3. Registering sessions with Supervisor
> 
> *Benefits:* Zero latency overhead, distributed parsing, scalable to 100+ agents, enforcement via pre-deployment certification.

#### Core Deliverables

**1. ReasoningPipe Standard Library**
* [ ] Implement `app/lib/reasoning_pipe.py` with core methods:
  * [ ] `log_thought(content, timestamp)` - Record reasoning steps
  * [ ] `log_action(action, details)` - Record concrete actions
  * [ ] `log_result(result, metrics)` - Record final output
  * [ ] `finalize()` - Write to permanent storage
* [ ] Standardized file format: `ReasoningPipe_{agent}_{session}.md`
* [ ] Session metadata: model, tier, duration, tokens, cost
* [ ] Automatic archival to `ReasoningPipe_{agent}.md` on finalize

**2. Supervisor Components**
* [ ] **Certifier** (`app/services/supervisor/certifier.py`):
  * [ ] Static analysis: Code structure validation
  * [ ] Dynamic testing: Run standardized test task
  * [ ] Output validation: Verify ReasoningPipe format
  * [ ] Certificate issuance: 30-day validity, SHA-256 signature
* [ ] **Guardian** (`app/services/supervisor/guardian.py`):
  * [ ] Runtime enforcement: Reject uncertified agents
  * [ ] Session tracking: Monitor active sessions
  * [ ] Lifecycle management: session_start/end notifications
* [ ] **Auditor** (`app/services/supervisor/auditor.py`):
  * [ ] Monthly quality audits: Score output compliance
  * [ ] Re-certification triggers: Flag agents below threshold
  * [ ] Statistics dashboard: Agent performance metrics

**3. Agent Wrapper Framework**
* [ ] Base wrapper class (`app/wrappers/base_wrapper.py`):
  * [ ] Abstract interface for all agents
  * [ ] Automatic supervisor protocol handling
  * [ ] Standardized execution flow
* [ ] Certified wrappers for initial launch:
  * [ ] `gemini_wrapper.py` - Gemini 2.0 Flash Thinking (L3)
  * [ ] `claude_wrapper.py` - Claude Sonnet 4.5 Thinking (L3)
  * [ ] `ollama_wrapper.py` - Local models (codellama:7b, etc.) (L1)
  * [ ] `deepinfra_wrapper.py` - Qwen2.5-Coder (L2)

**4. Testing & Validation**
* [ ] Unit tests (`tests/test_spec_008_reasoning_pipes.py`):
  * [ ] ReasoningPipe class: All methods tested
  * [ ] File format validation: Markdown correctness
  * [ ] Timestamp ordering: Chronological verification
* [ ] Certification tests (`tests/test_wrapper_certification.py`):
  * [ ] Static analysis: Code structure checks
  * [ ] Dynamic execution: Test task completion
  * [ ] Output validation: Format compliance
  * [ ] Certificate management: Issuance/expiration/revocation
* [ ] Integration tests (`tests/integration/test_reasoning_pipe_e2e.py`):
  * [ ] Full workflow: Certification → Execution → Audit
  * [ ] Multi-agent sessions: Concurrent execution
  * [ ] Error handling: Uncertified agent rejection
  * [ ] Performance: < 5% latency overhead from logging

**5. Documentation**
* [ ] Specification: `docs/008_reasoning_pipes.md` (v6.0.0) ✅
* [ ] Developer guide: `docs/WRAPPER_DEVELOPMENT_GUIDE.md`
* [ ] Update existing specs:
  * [ ] `005_development_protocols.md` → v6.0.0
  * [ ] `007_model_governance.md` → v6.0.0 (wrapper integration)

#### Completion Verification

**Pre-Flight Checklist:**
```bash
# 1. Verify all wrappers certified
python app/services/supervisor/certifier.py --list
# Expected: 4 agents (Gemini, Claude, Ollama, DeepInfra) with valid certs

# 2. Run specification tests
python tests/run_spec_tests.py --spec 008
# Expected: 100% pass rate

# 3. Run certification tests
pytest tests/test_wrapper_certification.py -v
# Expected: All certification workflow tests pass

# 4. Run integration tests
pytest tests/integration/test_reasoning_pipe_e2e.py -v
# Expected: E2E workflow tests pass

# 5. Verify ReasoningPipe output
ls -lh docs/journals/ReasoningPipe_*.md
# Expected: Session files created with valid format
```

**Acceptance Criteria:**
- [ ] All 4 initial wrappers certified and operational
- [ ] Test suite: 100% pass rate (unit + integration)
- [ ] Performance: ReasoningPipe logging < 5% overhead
- [ ] Documentation: Complete developer guide for new wrapper creation
- [ ] Docker integration: Certification works in containerized environment
- [ ] Nexus Dashboard: Agent certification status displayed

**Phase 6 Targets:**
- **Models Certified**: 4 (Gemini, Claude, Ollama base, DeepInfra)
- **Test Coverage**: 95%+ for reasoning_pipe.py and supervisor components
- **Certification Time**: < 60 seconds per wrapper
- **Monthly Audit**: Automated, < 10 minutes for all agents

### PHASE 7: ADVANCED KNOWLEDGE INDEXING
**Critical Decision Needed:**
> **The Graph Architecture:** Are we introducing a dedicated Graph Database (e.g., Neo4j) for relational mapping, or simulating specific graph edges via metadata in the existing Qdrant vector payloads?
> * *Impact:* Neo4j adds significant Docker weight and VRAM usage. Qdrant is lighter but less query-flexible.

* [ ] **From Semantic Keys to Knowledge Indexes:** Refactor the ingestion pipeline toward structured, concept-aware indexing.
* [ ] **Hierarchical Summarization:** Deploy the **Gravitas Librarian** to generate "Big Picture" summaries of all local documentation.
* [ ] **Relational Mapping:** Implement entity extraction to map dependencies between code files and architectural decisions.

**Completion Requirements:**
- [ ] Specs updated: `002_vector_memory.md`, new `009_knowledge_indexing.md`
- [ ] Test suite: `test_spec_009_knowledge_indexing.py`, Librarian tests
- [ ] Docker verification: Indexing pipeline works with Qdrant in Docker
- [ ] Performance: Knowledge graph queries execute efficiently

### PHASE 8: AGENT SPECIALIZATION (THE SCOUT'S EXPANSION)
**Critical Decision Needed:**
> **The Interaction Layer:** For "Live Web Probing," do you require a full Headless Browser (Playwright) for deep interaction, or is a Search API (SerpApi) sufficient?
> * *Impact:* Headless browsers require massive container resources (CPU/RAM). APIs are lightweight but text-only.

* [ ] **Multimodal Transcription:** Integrate `yt-dlp` and `Whisper` to allow the **Gravitas Scout** to ingest YouTube and audio sermons.
* [ ] **Live Web Probing:** Implement live web search for the **Gravitas Scout**.
* [ ] **L3 Feedback Loop:** Formalize the **Gravitas Scout**'s ability to "Ask L3" iterative reasoning questions.

**Completion Requirements:**
- [ ] Specs updated: `001_core_architecture.md`, new `010_agent_specialization.md`
- [ ] Test suite: `test_spec_010_agent_specialization.py`, Scout integration tests
- [ ] Docker verification: Audio transcription works in container
- [ ] Integration: Scout agent tested with real YouTube/audio content

### PHASE 9: GRAVITAS AGENTIC INFRASTRUCTURE
* [ ] **Mirroring Construction Protocols**: Research and implement a `.gravitas_agent` directory for each Gravitas Agent (**Gravitas Scout**, **Gravitas Librarian**, etc.).
* [ ] **Standardized Startup**: Implement a `recon` phase for Gravitas Agents to ensure they sync with global project state.

**Completion Requirements:**
- [ ] Specs updated: `005_development_protocols.md`, new `011_agentic_infrastructure.md`
- [ ] Test suite: `test_spec_011_agentic_infrastructure.py`, recon protocol tests
- [ ] Docker verification: Agent startup sequences tested in Docker
- [ ] Integration: All agents follow standardized protocols

### PHASE 10: INTELLIGENCE AUDIT & BENCHMARKING
* [ ] **Bi-Weekly Model Pulse:** Establish an automated sweep (every 14 days) of Ollama, DeepInfra, and Google for new model releases.
* [ ] **Independent Test Suite:** Develop a project-specific benchmarking suite to validate model performance against Gravitas RAG and code synthesis tasks before promotion to active roles.

**Completion Requirements:**
- [ ] Specs updated: `006_telemetry_calibration.md`, new `012_intelligence_audit.md`
- [ ] Test suite: `test_spec_012_intelligence_audit.py`, benchmark validation tests
- [ ] Docker verification: Automated model discovery works in Docker
- [ ] Performance: Benchmark suite produces consistent, reproducible results

---

## BACKLOG / TECH DEBT
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.
* [x] **Journal Rotation:** Implement dated journal snapshots for high-fidelity RAG ingestion. (Completed: `docs/journals/`)
* **VENV Hardening:** Standardize cross-platform dependency resolution in `requirements.txt`.