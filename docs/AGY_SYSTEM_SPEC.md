You are absolutely right. The previous code block broke because I nested a triple-backtick block (```) inside another triple-backtick block. This confuses the markdown renderer and cuts off the text (often around Section 5 or 6).

Here is the **AGY_SYSTEM_SPEC.md** enclosed in a **quadruple-backtick** block. This will render correctly so you can copy the entire thing, including the inner code blocks, without it breaking.

```markdown
# AntiGravity RAG - System Specification

**Version:** 3.1.0 (Agentic, RAG-Enabled, Secured)
**Status:** In Development / Dockerization Phase
**Repo:** [https://github.com/danflory/ragV2.git](https://github.com/danflory/ragV2.git)

## 1. Core Philosophy

The AntiGravity RAG is a **3-Layer Cognitive Pipeline** designed to balance speed, cost, and intelligence.

* **L1 (Reflex):** Local, Free, Fast. Runs on Titan RTX (24GB). Handles routine traffic and **Action Reflexes**.
* **L2 (Reasoning):** Cloud (DeepSeek/Qwen via DeepInfra). High IQ for complex logic and refactoring.
* **L3 (Deep Research):** Agentic flagship (Gemini 3 Pro). Used for deep document analysis and synthesis.

## 2. Architecture & Design Patterns

The system enforces **SOLID Principles** and **Modular Open Systems Approach (MOSA)** to ensure scalability and prevent "Split Brain" issues.

### 2.1 The Dependency Injection Flow

1. **Config:** Loads settings from `.env` using Pydantic.
2. **Container:** The central switchboard. It instantiates drivers and the **Memory Core**.
3. **Orchestrator:** The "Brain" that manages the RAG loop: Retrieve -> Augment -> Generate.
4. **Router:** The API entry point. Delegating to the Orchestrator or Container.

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
    * **Syntax Check:** `ast.parse()` ensures generated Python is valid.
    * **Secret Scanning:** Regex validation prevents committing `.env` keys or high-entropy strings.
    * **Destructive Command Blocklist:** Blocks `rm -rf`, `mkfs`, or modifying `.git` internals directly.
3.  **L2 Escalation (The Judge):**
    * If a diff exceeds **50 lines** or touches `core/*.py`, it triggers an asynchronous L2 Review.
    * *Action:* The Reflex is held; L2 approves/rejects; L1 is notified of the verdict.
4.  **Execution:** Only safe, validated actions are executed.

### 3.2 Git Hygiene
* **Pre-Commit Hook (Internal):** The system runs `ruff check` and `black --check` on the proposed file. If it fails, the commit is rejected, and L1 is ordered to fix syntax.
* **Atomic Rollback:** If a "Reflex" breaks the build (detected via `pytest` run), the system automatically reverts the last commit.

## 4. Technical Stack

* **Runtime:** Python 3.12+ (Docker on WSL2 / Ubuntu)
* **Vector DB:** ChromaDB (Persistent Storage via Docker Volume)
* **Embedder:** `sentence-transformers/all-MiniLM-L6-v2` (Local GPU Acceleration)
* **API Framework:** FastAPI (Async)
* **Containerization:** Docker Desktop w/ NVIDIA Container Toolkit (Hardware Unlocked)
* **Hardware Target:** NVIDIA Titan RTX (24GB VRAM), 32GB System RAM, 8 vCPUs

## 5. System Structure

```text
/rag_local
├── app/
│   ├── main.py          # Entry Point (Uvicorn)
│   ├── router.py        # API Routes (Reflex & Chat)
│   ├── container.py     # IoC Switchboard
│   ├── orchestrator.py  # RAG Pipeline Commander (Retrieve -> Generate)
│   ├── memory.py        # ChromaDB Wrapper (Long-term Memory)
│   ├── ingestor.py      # Codebase Ingestion & Shredding (Chunking)
│   ├── reflex.py        # Motor Functions (Git Sync / Shell Actions)
│   ├── safety.py        # NEW: Gatekeeper Logic (Linting, Scanning, Blocking)
│   ├── config.py        # Pydantic Settings
│   ├── database.py      # Low-level DB Connection & Logging
│   └── L1_local.py      # Local Driver (Ollama/HTTPX)
├── data/
│   └── chroma_db/       # Persistent Vector Store (Volume Mapped)
├── tests/               # Validation Suite
├── manage_memory.py     # Root CLI for Ingestion
├── docker-compose.yml   # Infrastructure Orchestrator
└── Dockerfile           # Environment Blueprint
```

## 6. RAG Implementation Details

### 6.1 Ingestion & Chunking

* **Strategy:** Sliding window chunking with overlap to preserve context at boundaries.
* **Parameters:** ~800 character chunk size with 100 character overlap.
* **File Hierarchy:** Hierarchical parsing prioritizing headings for better retrieval.

### 6.2 Retrieval & Augmentation

* **Top-K:** Retrieves the top 3 most relevant chunks per query.
* **Context Injection:** Code chunks are injected into the System Prompt before being sent to the LLM.

## 7. Development Rules

1. **Docker First:** All tests and execution should happen within the container.
2. **Verified Reflexes:** The Reflex System must pass the **Gatekeeper Check** (Lint + Secret Scan) before any commit. Unverified code is never pushed to origin.
3. **Atomic Commits:** Small, frequent commits are preferred over massive dumps.
4. **No SDK Bloat:** Use direct HTTP calls (`httpx`) over heavyweight SDK wrappers where possible.
5. **Contextual Awareness:** The AI must always look at the retrieved code context before answering architectural questions.

## 8. Project Roadmap & Status

| Status | Task | Description |
| :--- | :--- | :--- |
| **DONE** | L1/L2/L3 Drivers | Full 3-tier cognitive pipeline operational. |
| **DONE** | Reflex System | Git Add/Commit/Push automated via L1 intent. |
| **IN PROG** | Dockerization | Stable container with GPU passthrough and persistent volumes. |
| **TODO** | Gatekeeper Module | Implement `safety.py` for static analysis and secret scanning. |
| **TODO** | Memory Layer | ChromaDB integrated with automated code chunking. |
| **TODO** | **Memory Pruning** | **Automated cleanup of stale/deprecated chunks to prevent vector rot.** |
| **TODO** | **Auto-Formatter** | **Trigger `black` via Reflex before every Git Commit.** |
| **TODO** | Web Search | Integrate L3 with Tavily/DDG. Results must be summarized by L2 before Context Injection. |
| **TODO** | Frontend UI | Replace Curl with a simple web interface. |
| **TODO** | Requirements Ingest | Index project requirements for "Requirements-First" dev. |

```