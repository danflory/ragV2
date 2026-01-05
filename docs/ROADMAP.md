# GRAVITAS GROUNDED RESEARCH - STRATEGIC ROADMAP

## CURRENT STATE: v4.2.0 (GRAVITAS REBRAND)
The core infrastructure (Dockerized local RAG, Dual-GPU orchestration, Qdrant Memory + MinIO Storage, Postgres History) is stable and rebranding is complete.

---

## COMPLETED PHASES

### PHASE 1: THE FOUNDATION (QDRANT & MINIO)
* [x] **Hybrid Storage:** Split vectors (Qdrant) from blobs (MinIO) for hardware efficiency.
* [x] **Verification:** Full ingestion and search pipeline verified in `tests/`.

### PHASE 2: PERSISTENCE & TELEMETRY
* [x] **Infrastructure:** Provisioned `postgres_db` for chat history and metrics.
* [x] **Telemetry:** Implemented `app/telemetry.py` for VRAM tracking and system events.

### PHASE 3: THE GRAVITAS EVOLUTION (REBRANDING)
* [x] **Consistency:** Global rename of all legacy "agy" / "AntiGravity" terms to **Gravitas**.
* [x] **Automation:** Hooked session context generation into the system startup.
* [x] **Protocols:** Established `docs/GRAVITAS_NOMENCLATURE.md` and `docs/GRAVITAS_DEV_JOURNAL.md`.

---

## UPCOMING PHASES

### PHASE 4: COMMAND & CONTROL (THE NEXUS DASHBOARD)
* [ ] **Master Control Dashboard:** Unified Web UI for service management, model pulling, and system resets. **Includes integrated VRAM and Docker health metrics via Server-Sent Events (SSE)** for real-time monitoring.
* [ ] **Health API:** Implement `/health` endpoints for all containers to feed real-time status to the Nexus.

### PHASE 5: INTELLIGENCE OPTIMIZATION
* [ ] **Thought Latency Tracking:** Implement **driver-level instrumentation** in `app/L1_local.py`, `app/L2_network.py`, and `app/L3_google.py` to measure precise inference vs. network lag.
* [ ] **Dynamic Routing:** Use latency data to automatically switch models or layers based on real-time hardware performance.

### PHASE 6: ADVANCED KNOWLEDGE INDEXING
* [ ] **From Semantic Keys to Knowledge Indexes:** Refactor the ingestion pipeline to move beyond simple 1000-char chunks toward structured, concept-aware indexing.
* [ ] **Hierarchical Summarization:** Deploy the **Librarian Agent** to generate "Big Picture" summaries of all local documentation, creating a multi-tier index for both high-level strategy and granular retrieval.
* [ ] **Relational Mapping:** Implement entity extraction to map dependencies between code files and architectural decisions (e.g., linking `docs/journals/` entries to specific `app/` modules).

### PHASE 7: AGENT SPECIALIZATION (THE SCOUT'S EXPANSION)
* [ ] **Multimodal Transcription:** Integrate `yt-dlp` and `Whisper` (or similar) to allow the Scout to ingest YouTube lectures and audio sermon libraries.
* [ ] **Live Web Probing:** Implement a "Search Assistance" role for the Scout to conduct live web searches via SearxNG or Google Search API.
* [ ] **Hyper-Scraping:** Enable the Scout to scrape specific web targets for deep context retrieval, bypassing static memory limitations.
* [ ] **L3 Feedback Loop:** Formalize the Scout's ability to "Ask L3" questions for iterative reasoning during complex research tasks.

---

## BACKLOG / TECH DEBT
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.
* [x] **Journal Rotation:** Implement dated journal snapshots for high-fidelity RAG ingestion. (Completed: `docs/journals/`)
* **VENV Hardening:** Standardize cross-platform dependency resolution in `requirements.txt`.