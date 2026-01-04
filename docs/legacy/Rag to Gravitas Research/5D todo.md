# GRAVITAS WORK ORDER: PHASE 4.1 (Gravitas Grounded Research Migration)
# STATUS: URGENT
# CONTEXT: Moving from ChromaDB -> Qdrant (Vectors) + MinIO (Storage)

## 1. PRE-FLIGHT (Dependencies & Cleanup)
- [ ] **Delete Broken Tests:** Remove `tests/test_L1_fail.py` and `tests/test_L2_config.py`.
- [ ] **Update Dependencies:** Add `minio` and `qdrant-client` to `requirements.txt`.
- [ ] **Apply Interfaces:** Overwrite `app/interfaces.py` with the "Golden Source" provided by Architect.

## 2. THE STORAGE LAYER (MinIO)
- [ ] **Create `app/storage.py`:** Implement `MinioConnector` adhering to `ObjectStore` interface.
- [ ] **Create Test:** `tests/test_minio_storage.py`. Verify `upload()` and `get()` against a mock or live container.

## 3. THE MEMORY LAYER (Qdrant)
- [ ] **Refactor `app/memory.py`:**
    - Remove `chromadb` imports.
    - Implement `QdrantVectorStore` class inheriting from `VectorMemory`.
    - **Injection:** Constructor MUST accept a `storage: ObjectStore` instance.
    - **Logic:** `ingest()` -> Upload to MinIO first -> Upsert to Qdrant second.
- [ ] **Update Test:** Refactor `tests/test_memory_logic.py` to use `QdrantVectorStore`.

## 4. THE WIRING (Container)
- [ ] **Update `app/container.py`:**
    - Initialize `MinioConnector`.
    - Inject it into `QdrantVectorStore`.
    - Update `Container` to expose correct attributes (fix any `get_` method discrepancies).

## 5. EXIT CRITERIA
- [ ] **Run Suite:** `pytest tests/` (Expect `test_minio_storage.py` and `test_memory_logic.py` to PASS).
- [ ] **Generate Receipt:** Create `completed_phase4.1.md`.