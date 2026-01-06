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

### PHASE 7: ADVANCED KNOWLEDGE INDEXING
- [ ] **Hierarchical Summarization:** Deploy **Gravitas Librarian** for global documentation synthesis.
- [ ] **Relational Mapping:** Implement entity extraction for dependency mapping across the repo.
- [ ] **Decision Point:** Introduce Graph Database (Neo4j) vs. Metadata-only graph simulation.
- [ ] **Performance:** Ensure efficient knowledge graph queries.

### PHASE 8: AGENT SPECIALIZATION (THE SCOUT'S EXPANSION)
- [ ] **Multimodal Transcription:** Integrate `yt-dlp` and `Whisper` for audio/video ingestion.
- [ ] **Live Web Probing:** Implement live search for **Gravitas Scout**.
- [ ] **Decision Point:** Headless Browser (Playwright) vs. Lightweight Search API (SerpApi).
- [ ] **Iterative Reasoning:** Formalize "Scout-to-L3" iterative feedback loops.

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