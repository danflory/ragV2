# GRAVITAS WORK ORDER: PHASE 4.1 (Gravitas Grounded Research Migration)
# STATUS: URGENT

## 1. PRE-FLIGHT
- [ ] **Verify Dependencies:** Ensure `minio` and `qdrant-client` are active in the environment.
- [ ] **Apply Artifacts:** Update `app/interfaces.py` with the "Golden Source".

## 2. THE STORAGE LAYER (MinIO)
- [ ] **Create `app/storage.py`:** Implement `MinioConnector` adhering to `ObjectStore`.
- [ ] **Create Test:** `tests/test_minio_storage.py` (Verify upload/download loop).

## 3. THE MEMORY LAYER (Qdrant)
- [ ] **Refactor `app/memory.py`:**
    - Delete `ChromaDB` logic.
    - Implement `QdrantVectorStore(VectorMemory)`.
    - **Injection:** Constructor MUST accept `storage: ObjectStore`.
    - **Logic:** `ingest()` -> Upload to MinIO first -> Upsert to Qdrant second.
    - **TDD:** Update `tests/test_memory_logic.py` to use Qdrant+MinIO mocks.

## 4. THE SWITCHBOARD (Wiring)
- [ ] **Update `app/container.py`:**
    - Initialize `MinioConnector` using `config` values.
    - Inject `MinioConnector` into `QdrantVectorStore`.
    - **Verify:** Run `tests/test_ioc_refactor.py`.

## 5. EXIT CRITERIA
- [ ] **Run Suite:** `pytest tests/` (Expect `test_minio_storage.py` and `test_memory_logic.py` to PASS).
- [ ] **Receipt:** Generate `completed_phase4.1.md` with test logs.