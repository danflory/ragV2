# GRAVITAS GROUNDED RESEARCH - STRATEGIC ROADMAP
> **Vision**: Transform from a single-user RAG system into a secure, multi-agent "Knowledge Factory" (The Agentic Enterprise).

## CURRENT STATUS (v6.0.0 - REASONING PIPES)
- **Active Phase:** Phase 6 (Reasoning Pipes) - *Partially Complete*
- **Next Up:** Phase 6.5 (The Conceptual Shift) - *Infrastructure Alignment*
- **History:** Completed Phases 1-5 are archived in `docs/archived/COMPLETED_PHASES_1-5.md`.

---

## ACTIVE PHASES

### PHASE 6: SELF-LEARNING DATA (REASONING PIPES)
**Target**: Enable wrapper-certified reasoning capture for L1, L2, and L3 models.
- [x] **Core Infrastructure:** ReasoningPipe Library, Supervisor Guardian, Markdown Protocol.
- [x] **Certification System:** Wrapper Certifier, Certificate Issuance, Compliance Auditor.
- [x] **Agent Wrappers:** L3 Frontier (Gemini/Claude), L2 Specialized, L1 Local.
- [x] **Validation:** Spec tests, Certification workflow, Performance audit.
- [x] **Verification:** All tests passed. (Phase considered technically complete, moving to optimization).

### PHASE 6.5: THE CONCEPTUAL SHIFT (Codebase Alignment) - ✅ CORE COMPLETE
**Objective:** Align backend architecture (Registry, DB, Infrastructure) with the Gravitas Meta-Model.
- [x] **Ghost Registry:** Create `app/services/registry/ghost_registry.py` to map Identities to Shells.
- [x] **Shell Registry:** Rename `agent_registry.py` to `shell_registry.py` and strictly catalog Models.
- [x] **Backward Compatibility:** Create `agent_registry.py` facade with deprecation warnings.
- [x] **DB Alignment:** Update Postgres `history` table with `ghost_id` and `shell_id` columns (98 records backfilled).
- [x] **Infrastructure:** Rename `rag_app` to `gravitas_lobby` in `docker-compose.yml`.
- [x] **Artifacts:** Update `ReasoningPipe` to name journals by Ghost Identity.
- [ ] **Refactor:** Move orphaned `scripts/` into Agent Tool definitions (Deferred to Phase 7).
- [ ] **Refactor:** Remove routing logic from `app/router.py` (Deferred - requires Supervisor refactor).

---

## STRATEGIC HORIZON (THE AGENTIC ENTERPRISE)

### PHASE 7: THE SECURITY TIER (GATEWAY TO ENTERPRISE)
*Infrastructure hardening before scaling.*
- [ ] **7.1 The Security Officer:** Implement Access Control Policy engine (`access_groups`).
- [ ] **7.2 The Security Cop:** Implement Runtime enforcement and audit logs.
- [ ] **7.3 Identity Management:** JWT-based Auth and "Badge" System for Agents.

### PHASE 8: THE ACQUISITION TIER (THE HORSES)
*Equipping the Scout with real power.*
- [ ] **8.1 Scout Engine Upgrade:** Migrate Scout to `gemini-2.0-flash`.
- [ ] **8.2 The Crawler:** Implement `GravitasCrawler` (Headless Browser).
- [ ] **8.3 The Transcriber:** Implement `GravitasMiner` with `yt-dlp` + Whisper.
- [ ] **8.4 The OCR Specialist:** Implement Tesseract pipeline for PDF ingestion.

### PHASE 9: THE REFINEMENT TIER (THE TWO HEMISPHERES)
*Building the Theology Engine.*
- [ ] **9.1 Neo4j Integration:** Deploy Graph DB container alongside Qdrant.
- [ ] **9.2 Dual-Write Protocol:** Update Librarian to write to R-Brain (Vectors) and L-Brain (Graph).
- [ ] **9.3 Graph RAG:** Implement multi-hop retrieval logic.

### PHASE 10: THE WRITERS GUILD (THE ARTISTS)
*Specialized Output Engines.*
- [ ] **10.1 The Persona Engine:** Framework for defining Agent Personality (Tone, Vocabulary).
- [ ] **10.2 The Tech Writer:** Implement the "Private Room Interface" agent.
- [ ] **10.3 The Author:** Implement Long-Context book writing pipeline.

### PHASE 11: THE OFFICE (USER EXPERIENCE)
*The "VSCode for Knowledge" UI.*
- [ ] **11.1 The Lobby:** Public-facing dashboard with "Chat Twins" (Simulation Mode).
- [ ] **11.2 The Workbench:** "Dark Mode" IDE interface (Monaco Editor Integration).
- [ ] **11.3 The Vaults:** Multi-tenant storage logic (User ID separation).

### PHASE 12: THE AGENTIC MARKETPLACE
*Scaling the workforce.*
- [ ] **12.1 Agent Registry 2.0:** Dynamic loading of Agent Profiles from YAML.
- [ ] **12.2 Brain Swapping:** Hot-swap logic for upgrading Agent Models.
- [ ] **12.3 The "Cooler":** Intra-agent messaging bus for social simulation.

---

## BACKLOG / TECH DEBT
- [x] **SecurityCop:** Scan codebase for hardcoded keys (Secret Hygiene).
- [x] **Journal Rotation:** Implement dated journal snapshots. (Done: `docs/journals/`)
- [x] **GravitasEngineer:** Standardize cross-platform dependency resolution (VENV Hardening).
- [x] **GravitasEngineer:** Improve global exception handling for high-latency storage operations.