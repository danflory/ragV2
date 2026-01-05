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
* [ ] **Master Control Dashboard:** Transition from CLI-heavy scripts to a unified Web UI for service management, model pulling, and system resets.
* [ ] **Health API:** Implement `/health` endpoints for all containers to feed real-time status to the Nexus.

### PHASE 5: INTELLIGENCE OPTIMIZATION
* [ ] **Thought Latency Tracking:** Add telemetry metrics to measure processing time for L1 (Reflex), L2 (Reasoning), and L3 (Agentic) layers.
* [ ] **Dynamic Routing:** Use latency data to automatically switch models or layers based on real-time hardware performance.

---

## BACKLOG / TECH DEBT
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.
* **Journal Rotation:** Implement dated journal snapshots for high-fidelity RAG ingestion.
* **VENV Hardening:** Standardize cross-platform dependency resolution in `requirements.txt`.