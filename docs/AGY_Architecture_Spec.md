# AntiGravity RAG: Dual-GPU Gravitas Grounded Research Architecture Specification
**Version:** 4.0.0 (Gravitas Grounded Research / Dual-GPU / Production-Scale)
**User:** Dan
**Host:** Windows 11 Pro / WSL2 (Ubuntu)
**Primary Compute:** NVIDIA Titan RTX (24GB VRAM) + GTX 1060 (6GB VRAM)

---

## 1. Core Philosophy: The 3L Architecture
The system maximizes "Inference Economy" by cascading requests through three layers of progressive cost and capability, enhanced with Dual-GPU processing and Hybrid Vector Search.

### The Layers
* **L1 (Local Core):** `gemma2:27b-instruct-q4_k_m` via Ollama (GPU 0 - Titan RTX).
    * *Role:* Immediate, free, privacy-first inference with 27B parameter reasoning.
    * *Constraint:* 24GB VRAM with 7GB headroom for extended conversations.
* **L2 (Network Tier):** `Qwen2.5-Coder-32B-Instruct` via DeepInfra.
    * *Role:* Failover safety net and high-speed cloud fallback with 32B parameter coding expertise.
    * *Trigger:* Activated automatically if VRAM < 2GB or L1 times out.
* **L3 (Reasoning Tier):** Gemini 3 Pro (Vertex AI).
    * *Role:* Strategic planning and complex cross-domain reasoning (Configured but Dormant).

---

## 2. Hardware "Rules of Engagement"
The system implements **Dual-GPU Architecture** for optimal resource utilization:

### GPU 0: NVIDIA Titan RTX (24GB VRAM)
**Role:** Primary Compute / Generation
**Services:** `agy_ollama` (Port 11434)
**Models:** `gemma2:27b-instruct-q4_k_m` (~17GB VRAM)

### GPU 1: NVIDIA GeForce GTX 1060 (6GB VRAM)
**Role:** Dedicated Embedding Engine
**Services:** `agy_ollama_embed` (Port 11435)
**Models:** `nomic-embed-text-v1.5`, `BAAI/bge-m3`, `BAAI/bge-reranker-v2-m3`

---

## 3. Software Architecture

### Backend (FastAPI)
* **Port:** 5050
* **Environment:** Python 3.12 (Docker Container)
* **Key Modules:**
    * `router.py`: The "Brain". Orchestrates Logic -> Memory -> Model with RAG integration.
    * `memory.py`: The "Hippocampus". Manages Postgres (Short-term) and Qdrant (Long-term Hybrid Search).
    * `L1_local.py`: Driver for local Ollama instance with VRAM overload protection (Async HTTP).
    * `L2_network.py`: Driver for Cloud DeepInfra with retry logic (Async HTTP).

### Memory Systems
* **Short-Term:** `chat_history` (Postgres).
    * Stores raw chat logs (User/Assistant pairs).
    * Limit: Last 25 turns (configurable in `config.py`).
* **Long-Term:** `qdrant` (Hybrid Vector Search).
    * Stores vector embeddings with Dense + Sparse search via BGE-M3.
    * Retrieval: Fetches top 3 relevant chunks per query with BGE-Reranker precision.

---

## 4. Microservices Architecture

| Service | Container | GPU | Port | Purpose |
|---------|-----------|-----|------|---------|
| `gravitas_mcp` | `agy_mcp` | - | 8000 | Main Application (Sleep Infinity) |
| `ollama` | `agy_ollama` | 0 | 11434 | Generation (Gemma-2-27B) |
| `ollama_embed` | `agy_ollama_embed` | 1 | 11435 | Embeddings (Nomic/BGE) |
| `qdrant` | `agy_qdrant` | - | 6333 | Vector DB (Hybrid Search) |
| `minio` | `agy_minio` | - | 9000/9001 | Object Storage |
| `postgres_db` | `agy_postgres` | - | 5432 | Chat History & Telemetry |

---

## 5. Advanced Features
* **Hybrid Vector Search:** Dense (semantic) + Sparse (lexical) via Qdrant
* **Memory Hygiene:** Automatic pruning of stale chunks to prevent vector rot
* **Circuit Breaker:** GPU embedding with CPU fallback for resilience
* **VRAM Overload Protection:** OverloadError exceptions with telemetry logging
* **Git Resilience:** Authentication handling and tool presence detection
* **TDD Compliance:** Red-Green-Refactor development with comprehensive test coverage
