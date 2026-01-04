
System Audit Complete. I have a full holographic view of the Gravitas v4.0 state.

The Conflict: SIDE CAR.md demands deepseek-coder-v2 (16B) on GPU 0, while AGY_HARDWARE_CTX.md demands gemma2:27b.

The Gap: TEST_AUDIT.md explicitly flags that test_memory_logic.py is still testing ChromaDB, not Qdrant, and MinIO coverage is 0%.

The VRAM Reality: You have 24GB. You need ~26GB to run both models.

Step 1: The Constitution (patterns.md)
Action: I have finalized the "Law" to resolve the VRAM conflict via State Management and enforce the Qdrant/MinIO migration. Requirement: You must approve this document. Once approved, it dictates all future code written by the Agent.

# GRAVITAS ARCHITECTURAL CONSTITUTION (patterns.md)
# STATUS: FINAL PENDING APPROVAL
# VIOLATION STRATEGY: IMMEDIATE REJECTION

## 1. THE HARDWARE STATE MACHINE (VRAM Safety)
* **Context:** Titan RTX (24GB) cannot host `gemma2:27b` (RAG) and `deepseek-coder-v2:16b` (Dev) simultaneously.
* **Law:** The system operates in **Mutually Exclusive Modes**.
    * **State A (RAG_MODE):** `gemma2:27b` Loaded. Purpose: Chat, Research, Reflex.
    * **State B (DEV_MODE):** `deepseek-coder-v2` Loaded. Purpose: IDE Autocomplete, Sidecar.
* **Enforcement:** The `Container` must expose a `switch_mode(mode: str)` method that explicitly *unloads* the current model before pulling the new one.

## 2. THE Gravitas Grounded Research SEPARATION (The Memory Pattern)
* **Principle:** "Vectors are Indices; Files are Blobs."
* **Law:**
    1.  **Vector Store (Qdrant):** Stores *Embeddings* + *Metadata* (path, page_num) ONLY.
    2.  **Object Store (MinIO):** Stores the *Raw Text content*.
* **Anti-Pattern:** Storing the full 8k-token text chunk inside the Qdrant JSON payload. (Wastes RAM/Network).
* **Migration:** All legacy ChromaDB code in `app/memory.py` is deprecated.

## 3. THE SWITCHBOARD (Dependency Injection)
* **Law:** No class may instantiate `QdrantClient`, `MinioClient`, or `Ollama` drivers directly.
* **Enforcement:** All external services MUST be injected via `app.container.Container`.

## 4. THE GATEKEEPER (Security)
* **Law:** All "Reflex" actions (Shell/Git) must pass `app.safety.validate()`.
* **Constraint:** No `subprocess.run` allowed outside of `app.reflex`.

## 5. THE BUILDER'S CONTRACT (TDD)
* **Law:** No feature code without a failing `pytest` entry.
* **Exit Criterion:** A task is only "Done" when the `completed.md` receipt includes the passing test log.