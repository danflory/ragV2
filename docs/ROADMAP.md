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