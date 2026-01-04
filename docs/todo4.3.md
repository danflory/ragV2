# GRAVITAS WORK ORDER: PHASE 4.3 (The Ingestion Engine)
# STATUS: QUEUED
# CONTEXT: Connecting the File System to the new Omni-RAG Memory.

## 1. PRE-FLIGHT
- [ ] **Review `app/container.py`:** Note that `DocumentIngestor` is initialized with `vector_store` AND `storage`.

## 2. THE INGESTOR (Refactor)
- [ ] **Refactor `app/ingestor.py`:**
    - Update `__init__` to accept `vector_store: VectorMemory` and `storage: ObjectStore`.
    - **Logic:**
        - Walk `DOCS_PATH` (recursive).
        - Filter for `.md`, `.txt`, `.py`.
        - Chunk content (keep simple 1000-char chunks for now).
        - **Crucial:** Call `self.vector_store.ingest(text, metadata)` for each chunk.
    - **Logging:** Use `logger.info` to track progress (e.g., "Ingested file.md: 5 chunks").

## 3. THE TRIGGER (API)
- [ ] **Update `app/router.py`:**
    - Ensure `POST /ingest` calls the new `ingestor.ingest_all()`.
    - (Optional) Make it a background task if you want to be fancy, but blocking is fine for MVP.

## 4. VERIFICATION (TDD)
- [ ] **Create `tests/test_ingestion_pipeline.py`:**
    - Mock `vector_store.ingest`.
    - Create a temporary directory with dummy `.md` files.
    - Run `ingestor.ingest_all()`.
    - **Assert:** Verify `vector_store.ingest` was called N times.

## 5. EXIT CRITERIA
- [ ] **Run Suite:** `pytest tests/test_ingestion_pipeline.py`.
- [ ] **Submission:** Paste:
    1.  `completed_phase4.3.md` (Receipt).
    2.  `app/ingestor.py` (The Code).