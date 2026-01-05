RAG development
Custom Gem
Here is the Work Order for Phase 9.

We are now executing the "Hardening & Documentation" phase. We will crystalize the knowledge of the entire v4.0 architecture into a single, authoritative manual: Gravitas_Grounded_Research.md. This ensures the system is not just built, but maintainable and usable


# GRAVITAS WORK ORDER: PHASE 9 (Documentation & Hardening)
# STATUS: COMPLETED
# CONTEXT: Consolidating system knowledge into a master manual.
# OBJECTIVE: Produce the definitive guide for Users and Developers.

## 1. PRE-FLIGHT (Cleanup)
- [x] **Audit `docs/`:** Identify legacy markdown files that contradict v4.0 (e.g., old Chroma instructions).
- [x] **Action:** Move legacy docs to `docs/legacy/` or delete them to prevent hallucination in future sessions.

## 2. THE MANUAL (`Gravitas_Grounded_Research.md`)
- [x] **Create `Gravitas_Grounded_Research.md`** in the root directory.
- [x] **Section 1: The Philosophy:** Explain "Grounded Research" (Omni-RAG, Governance, TDD).
- [x] **Section 2: Architecture (v4.0):**
    - Diagram the 3-Layer Brain (Reflex, Reason, Research).
    - Diagram the Dual-GPU Split (Titan vs 1060).
    - Diagram the Memory Flow (MinIO + Qdrant).
- [x] **Section 3: The Nexus Manual (User Guide):**
    - How to use RAG vs DEV modes.
    - How to trigger the Librarian (Night Shift).
    - How to deploy the Scout (Deep Research).
    - How to read the Financial HUD.
- [x] **Section 4: Developer Protocols:**
    - The "Receipt" Rule (No commit without `completed.md`).
    - The "Gatekeeper" Rule (Safety checks).
    - How to run the Test Suite.

## 3. SYSTEM HARDENING (The Final Polish)
- [x] **Update `app/main.py`:** Ensure the API title/description matches "Gravitas Grounded Research".
- [x] **Verify `requirements.txt`:** Ensure all used libraries (google-genai, minio, qdrant-client) are pinned.

## 4. EXIT CRITERIA
- [x] **Submission:** Paste:
    1.  `completed_phase9.md`.
    2.  `Gravitas_Grounded_Research.md` (The Artifact).