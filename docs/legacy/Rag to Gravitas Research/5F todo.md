# GRAVITAS WORK ORDER: PHASE 4.1 (Gravitas Grounded Research Migration)
# STATUS: URGENT
# CONTEXT: Moving from ChromaDB -> Qdrant (Vectors) + MinIO (Storage)

## 1. PRE-FLIGHT (Dependencies & Cleanup)
- [x] **Delete Broken Tests:** Remove `tests/test_L1_fail.py` and `tests/test_L2_config.py` (Legacy artifacts).
- [x] **Verify Dependencies:** Confirm `minio` and `qdrant-client` are installed (Reference: `requirements.txt`).
- [x] **Apply Interfaces:** Overwrite `app/interfaces.py` with the "Golden Source" provided by the Architect.

## 2. THE STORAGE LAYER (MinIO)
- [x] **Create `app/storage.py`:**
    - Implement `MinioConnector` class adhering to the `ObjectStore` interface.
    - **Methods:** `upload(key, data)`, `get(key)`.
- [x] **Create Test:** `tests/test_minio_storage.py`.
    - **Goal:** Verify successful upload and download of text blobs.

## 3. THE MEMORY LAYER (Qdrant Refactor)
- [x] **Refactor `app/memory.py`:**
    - **Action:** Remove all `chromadb` logic.
    - **Implement:** `QdrantVectorStore` inheriting from `VectorMemory`.
    - **Injection:** Constructor MUST accept a `storage: ObjectStore` instance.
    - **Logic:** `ingest()` must:
        1. Upload raw text to `storage` (MinIO).
        2. Generate embedding.
        3. Upsert Vector + Metadata to Qdrant (do NOT store raw text in payload).
- [x] **Update Test:** Refactor `tests/test_memory_logic.py` to target the new `QdrantVectorStore`.

## 4. THE WIRING (Container)
- [x] **Update `app/container.py`:**
    - **Initialize:** `MinioConnector` using `config` values.
    - **Inject:** Pass `MinioConnector` into `QdrantVectorStore`.
    - **Expose:** Ensure `container.memory` and `container.storage` are accessible.

## 5. EXIT CRITERIA
- [x] **Run Test Suite:** Execute `pytest tests/`.
    - **Expect:** `test_minio_storage.py` and `test_memory_logic.py` to PASS.
- [x] **Generate Receipt:** Create `completed_phase4.1.md` containing the passing test logs.