# GRAVITAS MIGRATION PROTOCOL: PHASE 4.1 (Omni-RAG)

**Mission:** Implement the "Split-Brain" Memory Architecture (Qdrant + MinIO).
**Constraint:** STRICT adherence to `patterns.md` and `interfaces.py`.

## 1. PRE-FLIGHT (Dependencies)
- [ ] **Update `requirements.txt`:** Add `minio`, `qdrant-client`.
- [ ] **Update `app/interfaces.py`:** Paste the *Architect Approved* code for `ObjectStore` and `VectorMemory`.

## 2. THE STORAGE LAYER (MinIO)
- [ ] **Create `app/storage.py`:**
    - Implement `MinioConnector(ObjectStore)`.
    - **TDD:** Create `tests/test_minio_storage.py` first. Verify upload/download loop.

## 3. THE MEMORY LAYER (Qdrant)
- [ ] **Refactor `app/memory.py`:**
    - Delete `ChromaDB` logic.
    - Implement `QdrantVectorStore(VectorMemory)`.
    - **Injection:** Constructor must accept `storage: ObjectStore`.
    - **Logic:** `ingest()` must call `storage.upload()` BEFORE `qdrant.upsert()`.
    - **TDD:** Update `tests/test_memory_logic.py` to use Qdrant+MinIO mocks.

## 4. THE SWITCHBOARD (Wiring)
- [ ] **Update `app/container.py`:**
    - Initialize `MinioConnector` from `config`.
    - Inject `MinioConnector` into `QdrantVectorStore`.
    - **Verify:** Run `tests/test_ioc_refactor.py`.

## 5. EXIT CRITERIA
- [ ] **Run Suite:** `pytest tests/` (All must pass).
- [ ] **Receipt:** Generate `completed_phase4.1.md` with test logs.