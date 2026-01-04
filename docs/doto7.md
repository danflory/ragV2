We are activating The Librarian, the first autonomous agent in the "Shift" architecture. Its mandate is to process raw data dumps, synthesize them into high-quality indices, and curate the Omni-RAG memory without human intervention.

# GRAVITAS WORK ORDER: PHASE 7 (The Librarian Agent)
# STATUS: QUEUED
# CONTEXT: Implementing the "Night Shift" Data Curator.
# OBJECTIVE: Auto-process raw files, generate summaries, and optimize Qdrant indices.

## 1. PRE-FLIGHT (Infrastructure)
- [x] **Create Directories:**
    - `data/inbox`: The drop-zone for new raw content (PDFs, raw text dumps).
    - `data/archive`: Where files go after processing.
    - `app/agents`: Directory for agent logic.

## 2. THE AGENT LOGIC (Librarian)
- [x] **Create `app/agents/librarian.py`:**
    - **Class:** `LibrarianAgent`.
    - **Dependencies:** Injected with `container` (needs L1 Driver, Storage, Memory).
    - **Method:** `summarize(text: str) -> str`.
        - Uses L1 (Reflex) to generate a dense summary/abstract of the content.
        - *Prompt:* "Compress the following text into a high-density summary for vector retrieval..."
    - **Method:** `process_inbox()`.
        1. Scan `data/inbox`.
        2. For each file:
            a. Upload Raw Content to MinIO (Blob).
            b. Generate Summary.
            c. Ingest **Summary** to Qdrant (Index).
            d. Move file to `data/archive`.
    - **Pattern Enforcement:** Ensure the Qdrant payload links to the MinIO blob, keeping the index light.

## 3. THE TRIGGER (API)
- [x] **Update `app/router.py`:**
    - Add `POST /agents/librarian/run`.
    - Returns: `{"files_processed": 5, "status": "success"}`.

## 4. THE INTERFACE (Dashboard)
- [x] **Update `dashboard/index.html`:**
    - Add a "LIBRARIAN" section in the Tools Pane.
    - Add button: "START NIGHT SHIFT (PROCESS INBOX)".
- [x] **Update `dashboard/app.js`:**
    - Bind button to `/agents/librarian/run`.

## 5. VERIFICATION (TDD)
- [x] **Create `tests/test_librarian.py`:**
    - Mock L1 response (don't run actual inference).
    - Create dummy file in `data/inbox`.
    - Run `process_inbox`.
    - **Assert:** File moved to `archive`, Blob in Storage, Vector in Memory.

## 6. EXIT CRITERIA
- [x] **Run Suite:** `pytest tests/test_librarian.py`.
- [x] **Submission:** Paste:
    1.  `completed_phase7.md` (Receipt).
    2.  `app/agents/librarian.py`.
    3.  `app/router.py` (Updated).