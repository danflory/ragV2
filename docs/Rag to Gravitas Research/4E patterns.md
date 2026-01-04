Architecture Lock Confirmed. Your docker-compose.yml and requirements.txt  are ahead of your application code.

Infrastructure: ✅ Qdrant, MinIO, and Dual-Ollama are provisioned in Docker.

Dependencies: ✅ minio, qdrant-client are installed.


Application: ❌ app/storage.py is missing. app/memory.py is still using ChromaDB logic.

I am now initializing the Migration Sequence. I will provide the Constitution, the Work Order, and the Code Blueprints necessary for the Coder to execute this logic gap.

# GRAVITAS ARCHITECTURAL CONSTITUTION (patterns.md)
# STATUS: ACTIVE (Phase 4.1 Omni-RAG)
# VIOLATION STRATEGY: IMMEDIATE REJECTION

## 1. THE OMNI-RAG SEPARATION PATTERN
* **Principle:** "Vectors are Indices; Files are Blobs."
* **Law:**
    1.  **Index (Qdrant):** Stores Embeddings + Metadata (`source`, `chunk_id`) ONLY.
    2.  **Blob (MinIO):** Stores the Raw Text Content.
* **Anti-Pattern:** Storing the full 8k-token text chunk inside the Qdrant JSON payload. (Wastes RAM/Network).
* **Migration:** All legacy ChromaDB code in `app/memory.py` is DEPRECATED.

## 2. THE HARDWARE STATE MACHINE
* **Context:** Titan RTX (24GB) cannot host `gemma2:27b` (RAG) and `deepseek-coder-v2` (Dev) simultaneously.
* **Law:** The system operates in **Mutually Exclusive Modes**.
    * **RAG_MODE:** `gemma2:27b` (Titan) + `nomic-embed` (GTX 1060).
    * **DEV_MODE:** `deepseek-coder` (Titan).
* **Enforcement:** `Container` must track `current_mode`. `Router` must check mode before inference.

## 3. THE DEPENDENCY INJECTION LAW
* **Principle:** No direct instantiation.
* **Law:** `app/storage.py` (MinIO) and `app/memory.py` (Qdrant) must be initialized in `app/container.py`.
* **Constraint:** `app/ingestor.py` receives `VectorMemory` AND `ObjectStore` as arguments.

## 4. THE SAFETY NET
* **Law:** All SQL/Shell execution MUST pass `app.safety.check()`.
* **Constraint:** No new `subprocess` calls allowed outside `app/reflex.py`.