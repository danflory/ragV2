This audit confirms the critical architectural drift: the code is running legacy logic (ChromaDB) while the spec demands Gravitas Grounded Research (Qdrant + MinIO).

I have finalized the Migration Plan.

1. The Constitution (patterns.md)
This document is now the law. It explicitly forbids the "Anti-Pattern" of storing raw text in vector payloads and enforces the Qdrant/MinIO split.


# GRAVITAS ARCHITECTURAL CONSTITUTION (patterns.md)
# STATUS: APPROVED FOR EXECUTION

## 1. THE MEMORY SEPARATION PATTERN (Gravitas Grounded Research)
* **Principle:** "Vectors are Indices; Files are Blobs."
* **Law:**
    1.  **Index:** `Qdrant` stores Embeddings + Metadata (Path, ChunkID).
    2.  **Blob:** `MinIO` stores the Raw Text Content.
* **Why:** Storing 8k-token text chunks in Qdrant Payload causes OOM.
* **Refactor Target:** `app/memory.py` MUST replace `ChromaDB` with `QdrantClient`.

## 2. THE HARDWARE STATE MACHINE
* **Context:** Titan RTX (24GB) is the shared resource.
* **Law:** The system has two exclusive modes:
    * **RAG_MODE:** `gemma2:27b` (Titan) + `nomic-embed` (GTX 1060).
    * **DEV_MODE:** `deepseek-coder` (Titan).
* **Enforcement:** `Container` must track `current_mode`. `Router` must check mode before inference.

## 3. THE DEPENDENCY INJECTION LAW
* **Principle:** No direct instantiation.
* **Law:** `app/storage.py` (MinIO) and `app/memory.py` (Qdrant) must be initialized in `app/container.py`.
* **Constraint:** `app/ingestor.py` receives `VectorStore` AND `ObjectStore` as arguments.

## 4. THE SAFETY NET
* **Law:** All SQL/Shell execution MUST pass `app.safety.check()`.
* **Constraint:** No new `subprocess` calls allowed outside `app/reflex.py`.