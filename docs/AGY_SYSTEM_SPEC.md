# AntiGravity RAG - System Specification
**Version:** 0.3.0 (Solid Foundation)
**Status:** Stable / Native Execution
**Repo:** https://github.com/danflory/ragV2.git

## 1. Core Philosophy
The AntiGravity RAG is a **3-Layer Cognitive Pipeline** designed to balance speed, cost, and intelligence.
- **L1 (Reflex):** Local, Free, Fast. Runs on Titan RTX (24GB). Handles ~80% of routine traffic.
- **L2 (Reasoning):** Cloud (DeepSeek/Claude/GPT). High IQ, cost-per-token. Used for escalation.
- **L3 (Deep Research):** Agentic. Long-running tasks, web search, synthesis. (Future)

## 2. Architecture & Design Patterns
The system strictly enforces **SOLID Principles** and **Inversion of Control (IoC)** to prevent "Split Brain" issues.

### 2.1 The Dependency Injection Flow
1. **Config:** Holds raw settings (via Pydantic).
2. **Container:** The *only* place where `Config` meets `Code`. Instantiates drivers.
3. **Router:** Asks the `Container` for services. Never imports drivers directly.
4. **Driver:** Receives config via `__init__`. Stateless.

### 2.2 The Interface Contract (`interfaces.py`)
All drivers (L1, L2, L3) must inherit from `LLMDriver` and implement:
- `async def generate(self, prompt: str) -> str`
- `async def check_health(self) -> bool`

## 3. Technical Stack
- **Runtime:** Python 3.12+ (WSL2 / Ubuntu)
- **API Framework:** FastAPI (Async)
- **Networking:** `httpx` (Direct HTTP calls, no SDK wrappers)
- **Inference Server:** Ollama (External Process on Host)
- **Hardware Target:** NVIDIA Titan RTX (24GB VRAM)

## 4. Current File Structure
```text
/rag_local
├── app/
│   ├── main.py          # Entry Point (Uvicorn)
│   ├── router.py        # API Routes (Delegates to Container)
│   ├── container.py     # IoC Switchboard (Wires Drivers)
│   ├── interfaces.py    # Abstract Base Classes
│   ├── config.py        # Pydantic Settings (Reads .env)
│   └── L1_local.py      # Concrete Driver (Ollama/HTTPX)
├── tests/
│   ├── test_ioc_refactor.py  # Verifies Driver Contracts
│   └── test_ioc_baseline.py  # Verifies Router Escalation
├── docs/
│   └── AGY_SYSTEM_SPEC.md    # THIS FILE
├── requirements.txt
└── .gitignore
```

## 5. Critical Configuration (Environment)
The application is configured via a `.env` file or System Environment Variables.

### 5.1 Required Variables (Keys)
| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Point to the Host's Ollama instance. |
| `MODEL` | `codellama:7b` | The active model tag. |
| `USER_NAME` | `Dan` | Used for system prompt context personalization. |
| `PORT` | `5050` | The port the FastAPI server listens on. |
| `VRAM_THRESHOLD_GB` | `2.0` | Minimum free GB required on Titan RTX before 16B+ models load. |

### 5.2 Hardware Guards
- **VRAM Guard:** `router.py` checks `GPUtil` before loading heavy models (e.g., `deepseek-coder-v2:16b`).
- **Networking:** In Native mode (current), use `127.0.0.1`. In Docker mode, use `host.docker.internal`.

## 6. Development Rules (For AI Agents)
1. **Never Hardcode Imports:** If you need a driver, get it from `app.container`.
2. **Respect the Interface:** If you add L2, you MUST implement `generate()` and `check_health()`.
3. **Async Everything:** All I/O (Network/DB) must be `async/await`.
4. **Test Driven:** If you refactor a core component, run `pytest tests/test_ioc_refactor.py` immediately.

## 7. Project Roadmap & Status
| Status | Task | Description |
| :--- | :--- | :--- |
| **DONE** | Environment Setup | WSL2, Python 3.12, venv, and dependencies installed. |
| **DONE** | Networking Fix | Resolved "Split Brain" between Windows host and WSL container. |
| **DONE** | Architecture Design | Defined 3-Layer (L1/L2/L3) logic and Interface contracts. |
| **DONE** | IoC Implementation | Created `container.py` to decouple Router from Drivers. |
| **DONE** | L1 Driver (Local) | Implemented `codellama:7b` driver with async `httpx`. |
| **DONE** | Hardware Guard | Added `GPUtil` checks to prevent VRAM OOM crashes. |
| **DONE** | Native Verification | Verified full pipeline (Curl -> API -> GPU) without Docker. |
| **DONE** | Version Control | Initialized Git, created `.gitignore`, pushed to GitHub `ragV2`. |
| **DONE** | Documentation | Created System Specification (`AGY_SYSTEM_SPEC.md`). |
| **DONE** | L2 Driver (Cloud) | Implement `L2_cloud.py` for Anthropic/DeepSeek API escalation. |
| **TODO** | Vector Database | Install ChromaDB and implement document ingestion. |
| **TODO** | RAG Logic | Connect Retrieval step before L1 Generation. |
| **TODO** | Frontend UI | Build a simple Streamlit or React interface (replace Curl). |
| **TODO** | Docker Stabilization | Fix WSL2 deadlock to enable full containerization. |
| **DONE** | L3 Agents | Implement autonomous web-search/deep-research agents. |
| **TODO** | CI/CD Pipeline | Automate testing on GitHub Actions. |