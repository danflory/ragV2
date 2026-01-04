# GRAVITAS MIGRATION PLAN: PHASE 4.1 (The Brain Transplant)

**Objective:** Replace Legacy Memory (Chroma) with Gravitas Grounded Research (Qdrant + MinIO).

## 1. Storage Layer (New Feature)
- [ ] **Create `app/storage.py`:**
    - Implement `MinioConnector` class.
    - Methods: `upload(key, text)`, `download(key)`.
    - **Test:** `tests/test_minio_storage.py` (Verify Upload/Download).

## 2. Vector Layer (Refactor)
- [ ] **Modify `app/memory.py`:**
    - Remove `chromadb` import. Add `qdrant_client`.
    - Implement `QdrantVectorStore`.
    - **Crucial:** `add_texts` method must now:
        1. Upload text to MinIO.
        2. Upload vector + MinIO Key to Qdrant.
    - **Test:** `tests/test_memory_logic.py` (Update for Qdrant).

## 3. Container Wiring (IoC)
- [ ] **Update `app/container.py`:**
    - Initialize `MinioConnector`.
    - Inject `MinioConnector` into `VectorStore` or `Ingestor`.
    - **Test:** `tests/test_ioc_refactor.py` (Verify container boots).

## 4. Ingestion Pipeline
- [ ] **Update `app/ingestor.py`:**
    - Switch to BGE-M3 logic (Dense + Sparse).
    - Ensure it calls the new `memory.add_texts` contract.

## 5. Verification
- [ ] **Run Full Suite:** `pytest tests/`
- [ ] **Generate Receipt:** `completed_phase4.1.md`