# AntiGravity RAG - System Specification

**Version:** 4.0.0 (Omni-RAG / Dual-GPU / Production-Scale)
**Status:** Production-Ready / Hybrid Search Operational
**Repo:** [https://github.com/danflory/ragV2.git](https://github.com/danflory/ragV2.git)

## 1. Core Philosophy

The AntiGravity RAG is a **Production-Grade Hybrid RAG Architecture** optimized for processing thousands of pages with precision retrieval. The system maximizes "Inference Economy" by cascading requests through three layers of progressive cost and capability.

* **L1 (Reflex):** Local, Free, Fast. Runs on Titan RTX (24GB). Handles routine traffic and **Action Reflexes**.
* **L2 (Reasoning):** Cloud (Qwen2.5-Coder-32B via DeepInfra). High IQ for complex logic and refactoring.
* **L3 (Deep Research):** Agentic flagship (Gemini 3 Pro). Used for deep document analysis and synthesis.

## 2. Architecture & Design Patterns

The system enforces **SOLID Principles** and **Modular Open Systems Approach (MOSA)** with **Dual-GPU Architecture** for optimal resource utilization.

### 2.1 The Dependency Injection Flow

1. **Config:** Loads settings from `.env` using Pydantic.
2. **Container:** The central switchboard. It instantiates drivers and manages system resources.
3. **Router:** The API entry point. Orchestrates Logic -> Memory -> Model with RAG integration.
4. **Memory Core:** Hybrid Vector Search with Qdrant and BGE-M3 models.

### 2.2 The Interface Contract (`interfaces.py`)

All drivers must inherit from `LLMDriver` to maintain interoperability:

* `async def generate(self, prompt: str) -> str`
* `async def check_health(self) -> bool`

## 3. Reflex Security (The "Gatekeeper" Protocol)

To prevent "hallucinated destruction" or secret leakage without hindering speed, all **Reflex Actions** (Shell/Git) must pass through a strict, automated safety filter.

### 3.1 The "Trust but Verify" Loop
Reflexes are not executed directly. They are **proposed** by L1 and **validated** by the Gatekeeper module before execution.

1.  **Proposal:** L1 generates a shell command or file write.
2.  **Static Analysis (The Filter):**
    * **Syntax Check:** Multi-format validation (`ast.parse()`, YAML/JSON validators, SQL blocking)
    * **Secret Scanning:** Regex validation prevents committing `.env` keys or high-entropy strings.
    * **Destructive Command Blocklist:** Blocks `rm -rf`, `mkfs`, or modifying protected system files.
3.  **L2 Escalation (The Judge):**
    * If a diff exceeds **50 lines** or touches `core/*.py`, it triggers an asynchronous L2 Review.
    * *Action:* The Reflex is held; L2 approves/rejects; L1 is notified of the verdict.
4.  **Execution:** Only safe, validated actions are executed.

### 3.2 Git Hygiene & Resilience
* **Pre-Commit Hook (Internal):** The system runs `ruff check` and `black --check` on the proposed file. If it fails, the commit is rejected, and L1 is ordered to fix syntax.
* **Atomic Rollback:** If a "Reflex" breaks the build (detected via `pytest` run), the system automatically reverts the last commit.
* **Authentication Resilience:** Graceful handling of Git auth failures in headless containers
* **Tool Resilience:** Cloud CLI detection with Python SDK guidance

## 4. Technical Stack

* **Runtime:** Python 3.12+ (Docker on WSL2 / Ubuntu)
* **Vector DB:** Qdrant (Hybrid Search via Docker Volume)
* **Embedder:** Dual models on GPU 1 (Nomic-Embed, BGE-M3, BGE-Reranker)
* **API Framework:** FastAPI (Async)
* **Containerization:** Docker Desktop w/ NVIDIA Container Toolkit (Hardware Unlocked)
* **Hardware Target:** Dual NVIDIA GPUs (Titan RTX 24GB + GTX 1060 6GB), 32GB System RAM, 8 vCPUs

## 5. System Structure

```text
/rag_local
├── app/
│   ├── main.py          # Entry Point (Uvicorn)
│   ├── router.py        # API Routes (Reflex & Chat with RAG)
│   ├── container.py     # IoC Switchboard
│   ├── memory.py        # Qdrant Hybrid Search + Reranker
│   ├── ingestor.py      # BGE-M3 Hybrid Embedding Pipeline
│   ├── reflex.py        # Motor Functions (Git Sync / Shell Actions + Resilience)
│   ├── safety.py        # Gatekeeper Logic (Linting, Scanning, Blocking)
│   ├── config.py        # Pydantic Settings
│   ├── database.py      # Postgres Connection & Logging
│   ├── L1_local.py      # Gemma-2-27B Driver (VRAM Overload Protection)
│   └── L2_network.py     # DeepInfra Driver (Retry Logic)
├── data/
│   ├── qdrant/          # Hybrid Vector Store (Volume Mapped)
│   ├── minio/           # Object Storage (Raw Documents)
│   └── postgres_data/    # SQL History (Chat + Telemetry)
├── tests/               # Validation Suite
├── docker-compose.yml   # Infrastructure Orchestrator
└── requirements.txt     # Python Dependencies
```

## 6. Hybrid RAG Implementation Details

### 6.1 Ingestion & Chunking

* **Strategy:** Sliding window chunking with overlap to preserve context at boundaries.
* **Parameters:** Configurable chunk size with 100 character overlap.
* **Memory Hygiene:** Automatic pruning of stale chunks to prevent vector rot.

### 6.2 Retrieval & Augmentation

* **Hybrid Search:** Dense (semantic) + Sparse (lexical) via BGE-M3
* **Reranking:** BGE-Reranker for precision hits
* **Context Injection:** Top results injected into LLM prompt

## 7. Development Rules

1. **Docker First:** All tests and execution should happen within the container.
2. **Verified Reflexes:** The Reflex System must pass the **Gatekeeper Check** (Lint + Secret Scan) before any commit.
3. **Atomic Commits:** Small, frequent commits are preferred over massive dumps.
4. **No SDK Bloat:** Use direct HTTP calls (`httpx`) over heavyweight SDK wrappers where possible.
5. **Contextual Awareness:** The AI must always look at the retrieved code context before answering architectural questions.
6. **TDD Compliance:** Red-Green-Refactor development with comprehensive test coverage

## 8. Advanced System Features

### 8.1 Memory Hygiene
* **Automatic Pruning:** Removes stale vector chunks to prevent "Vector Rot"
* **Source-Based Management:** Tracks document sources for clean updates

### 8.2 Circuit Breaker Patterns
* **GPU Resilience:** Falls back to CPU embedding on GPU failures
* **Graceful Degradation:** Maintains functionality during partial outages

### 8.3 Telemetry & Monitoring
* **VRAM Logging:** Continuous monitoring with OverloadError protection
* **Usage Statistics:** Detailed L1/L2 usage tracking in Postgres
* **System Events:** Comprehensive telemetry for performance analysis

## 9. Project Roadmap & Status

| Status | Task | Description |
| :--- | :--- | :--- |
| **DONE** | L1/L2/L3 Drivers | Full 3-tier cognitive pipeline operational. |
| **DONE** | Reflex System | Git Add/Commit/Push automated via L1 intent with resilience. |
| **DONE** | Dockerization | Stable container with GPU passthrough and persistent volumes. |
| **DONE** | Gatekeeper Module | Implemented `safety.py` for static analysis and secret scanning. |
| **DONE** | Memory Layer | Qdrant integrated with hybrid search and automated chunking. |
| **DONE** | Memory Pruning | Automated cleanup of stale/deprecated chunks to prevent vector rot. |
| **DONE** | Dual-GPU Architecture | Titan RTX for generation, GTX 1060 for embeddings. |
| **TODO** | Web Search | Integrate L3 with Tavily/DDG. Results must be summarized by L2 before Context Injection. |
| **TODO** | Frontend UI | Replace Curl with a simple web interface. |
| **TODO** | Requirements Ingest | Index project requirements for "Requirements-First" dev. |
