
2. The "VRAM Math" Reality Check
Your documents reveal a physical constraint that dictates our software architecture:

Available VRAM: 24 GB (Titan RTX)

Gemma-2-27B (Q4): ~16.5 GB

DeepSeek-Coder-V2-16B (Q4): ~9.0 GB

Combined Requirement: ~25.5 GB (OOM Crash)

Conclusion: The "Sidecar" described in DEEPSEEK_SIDECAR.md cannot run simultaneously with the RAG L1 (Gemma).

Pattern Required: The State Machine. The system must have explicit states (CODING_MODE vs. RAG_MODE) that unload one model before loading the other.

3. Draft: The Architectural Constitution (patterns.md)
Based on these 10 files, I have refined the patterns.md to explicitly handle the VRAM collision and the Qdrant migration.

# GRAVITAS ARCHITECTURAL CONSTITUTION (patterns.md)
# STATUS: DRAFT (Pending Approval)

## 1. THE SWITCHBOARD (IoC Container)
* **Law:** All dependencies (Qdrant, MinIO, Ollama) MUST be injected via `app.container`.
* **Violation:** Instantiating `QdrantClient` inside `router.py`.

## 2. THE HARDWARE STATE MACHINE (VRAM Safety)
* **Context:** Titan RTX (24GB) cannot host Coder + RAG simultaneously.
* **Law:** The system operates in mutually exclusive modes.
    * **MODE A (RAG/Reflex):** Loads `gemma2:27b`. For Chat & Query.
    * **MODE B (Dev/Sidecar):** Loads `deepseek-coder-v2:16b`. For IDE Autocomplete.
* **Enforcement:** `model_manager.py` must explicitly `unload()` the active model before `pull/load()` of the target.

## 3. THE Gravitas Grounded Research SEPARATION (Memory)
* **Law:** * **Vectors (Index):** Stored in **Qdrant** (GPU 1 optimized).
    * **Content (Blob):** Stored in **MinIO** (S3 Protocol).
* **Anti-Pattern:** Storing full document text in Qdrant Payload (wastes RAM).

## 4. THE GATEKEEPER (Security)
* **Law:** All "Reflex" actions (Shell/Git) must pass `app.safety.validate()`.
* **Constraint:** No `subprocess.run` allowed outside of `app.reflex`.

## 5. THE DUAL-GPU CONTRACT
* **Law:** * **GPU 0 (Titan):** Exclusive for Generation.
    * **GPU 1 (1060):** Exclusive for Embeddings (`nomic`, `bge-m3`).
* **Verification:** `tests/test_dual_gpu.py` must pass before any deployment.