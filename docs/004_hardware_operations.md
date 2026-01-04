# 004_HARDWARE_OPERATIONS.md
# STATUS: ACTIVE
# VERSION: 4.0.0 (Gravitas Grounded Research / Dual-GPU)

## 1. DUAL-GPU ARCHITECTURE
The system leverages **dual NVIDIA GPUs** for parallel processing and optimal resource utilization.

*   **GPU 0 (Titan RTX 24GB):** Primary Compute / Generation
    * **Role:** Dedicated AI Inference / Local LLM (L1) / Training
    * **Services:** `agy_ollama` (Port 11434)
    * **Models:** `gemma2:27b-instruct-q4_k_m` (~17GB VRAM)

*   **GPU 1 (GTX 1060 6GB):** Dedicated Embedding Engine
    * **Role:** Runs productive workloads instead of idle display duty
    * **Services:** `agy_ollama_embed` (Port 11435)
    * **Models:** `nomic-embed-text-v1.5`, `BAAI/bge-m3`, `BAAI/bge-reranker-v2-m3`

## 2. VRAM OVERLOAD PROTECTION
To prevent system crashes or OOM (Out Of Memory) during long context sessions, the system implements **OverloadError** exceptions:

1.  **Strict Buffer:** 2GB must remain free at all times.
2.  **Logic:** Prior to any L1 inference, `GPUtil` queries all GPUs.
3.  **Action:** If `Free_VRAM < 2GB` on any GPU, the request **must** be promoted to L2 to avoid crash.
4.  **Telemetry:** All VRAM checks logged to Postgres for monitoring and analysis.

## 3. MICROSERVICES TOPOLOGY
The system runs in a multi-container environment with dedicated services:

*   **`gravitas_mcp`:** Main application container with sleep infinity for manual process injection
*   **`agy_ollama`:** L1 model hosting (GPU 0 - Titan RTX)
*   **`agy_ollama_embed`:** Embedding models (GPU 1 - GTX 1060)
*   **`agy_qdrant`:** Hybrid vector database (CPU)
*   **`agy_minio`:** Object storage for raw documents (CPU)
*   **`postgres_db`:** Chat history and telemetry logging (CPU)

## 4. ADVANCED HARDWARE FEATURES
* **Parallel Processing:** Embeddings don't block generation
* **VRAM Optimization:** Frees 6-7GB on Titan RTX for larger context
* **Cost Efficiency:** GTX 1060 runs productive workloads instead of idle display duty
* **Circuit Breaker:** GPU embedding with CPU fallback for resilience
