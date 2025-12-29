# Google AntiGravity: 3L Toolchain Specification
**Version:** 0.5 (Foundation Phase)
**User:** Dan
**Host:** Windows 10 Pro / WSL (Ubuntu)
**Primary Compute:** NVIDIA Titan RTX (24GB VRAM)

---

## 1. Core Philosophy: The 3L Architecture
The system maximizes "Inference Economy" by cascading requests through three layers of progressive cost and capability.

### The Layers
* **L1 (Local Core):** `deepseek-coder-v2:16b` via Ollama.
    * *Role:* Immediate, free, privacy-first inference.
    * *Constraint:* 24GB VRAM Hard Limit.
* **L2 (Network Tier):** `gemini-flash-1.5` via OpenRouter.
    * *Role:* Failover safety net and high-speed cloud fallback.
    * *Trigger:* Activated automatically if VRAM < 4GB or L1 times out.
* **L3 (Reasoning Tier):** Gemini 3 Pro (Vertex AI).
    * *Role:* Strategic planning and complex cross-domain reasoning (Future Implementation).

---

## 2. Hardware "Rules of Engagement"
To prevent system crashes (OOM), the **Router** adheres to strict safety buffers:

1.  **VRAM Monitoring:** Before any L1 inference, `GPUtil` checks available VRAM.
2.  **The Safety Floor:** `4096MB` (4GB).
    * *Logic:* If Free VRAM < 4GB, the system **must** bypass L1 and force L2.
    * *Reason:* Context caching (KV Cache) for long chats can spike usage rapidly.

---

## 3. Software Architecture

### Backend (FastAPI)
* **Port:** 5050
* **Environment:** Python 3.12 (Virtual Env: `~/dev_env/rag_local/venv`)
* **Key Modules:**
    * `router.py`: The "Brain". Orchestrates Logic -> Memory -> Model.
    * `memory.py`: The "Hippocampus". Manages SQLite (Short-term) and ChromaDB (Long-term).
    * `L1_local.py`: Driver for local Ollama instance (Async HTTP).
    * `L2_network.py`: Driver for Cloud OpenRouter (Async HTTP).

### Memory Systems
* **Short-Term:** `memory.db` (SQLite).
    * Stores raw chat logs (User/Assistant pairs).
    * Limit: Last 25 turns (configurable in `config.py`).
* **Long-Term:** `rag_local/chroma_db` (ChromaDB).
    * Stores vector embeddings of Dan's project files and documentation.
    * Retrieval: Fetches top 2 relevant chunks per query.

---

## 4. Current File Map & Status

| File | Status | Responsibility |
| :--- | :--- | :--- |
| `app/main.py` | 🚧 Pending | Entry point; initializes server. |
| `app/router.py` | ✅ Active | Async routing logic with VRAM guard. |
| `app/memory.py` | ✅ Active | Async wrappers for SQLite/ChromaDB. |
| `app/L1_local.py` | ✅ Active | Connects to Ollama (Port 11434). |
| `app/L2_network.py`| ✅ Active | Connects to OpenRouter API. |
| `app/config.py` | ✅ Active | Central config class (Ports, Models). |
| `.env` | 🔒 Private | Holds `OPENROUTER_API_KEY`. |

---

## 5. Roadmap (Immediate Priorities)
1.  **Server Initialization:** Create `app/main.py` to launch the API.
2.  **UI Layer:** Connect a frontend (Open WebUI or VS Code) to `localhost:5050`.
3.  **Knowledge Ingestion:** Script to batch-read `docs/` and project files into ChromaDB.