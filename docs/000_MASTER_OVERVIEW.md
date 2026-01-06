# 000_MASTER_OVERVIEW.md
# STATUS: ACTIVE
# VERSION: 4.5.0 (Gravitas Command & Control / Telemetry Calibration)

## 1. CORE PHILOSOPHY
**Gravitas Grounded Research** is a **Dual-GPU Production-Grade Hybrid RAG Architecture**. The internal system orchestration, logic, and departmental specialists (the "Workers") all operate under the **Gravitas** namespace. The development and deployment of this project are managed by the external AI assistant, **Antigravity**.

*   **L1 (Reflex):** Zero-cost tier. Ollama/Titan RTX. Default for capable tasks.
*   **L2 (Edge):** Low-cost tier. DeepInfra. High-speed reasoning.
*   **L3 (Elite):** High-cost tier. Gemini 3 Pro. Deep research and architectural synthesis.

## 2. THE DUAL-GPU ARCHITECTURE
The system leverages **dual NVIDIA GPUs** for parallel processing and implements **Dense + Sparse hybrid vector search** via Qdrant.

*   **GPU 0 (Titan RTX 24GB):** Primary Compute / Generation (Gravitas Brain)
*   **GPU 1 (GTX 1060 6GB):** Dedicated Embedding Engine (Memory Indexer)

## 3. CORE DESIGN PRINCIPLES
1.  **Thinking Transparency:** Bit-for-bit faithfulness in reasoning logs via Reasoning Pipes.
2.  **Dual-Track Journaling:** Separation of Strategic (Executive) and Forensic (Reasoning) logs.
3.  **SOLID Architecture:** Enforced via `app/container.py` (IoC).
4.  **Test-Driven Development (TDD):** Red-Green-Refactor is the law.
5.  **Reflex Security:** All actions pass through the Gatekeeper (`app/safety.py`).
6.  **Inference Economy:** Cost-optimized routing based on 60-day performance telemetry.

## 4. DOCUMENTATION MAP
| ID | Document | Status | Scope |
| :--- | :--- | :--- | :--- |
| 000 | [MASTER_OVERVIEW](file:///home/dflory/dev_env/Gravitas/docs/000_MASTER_OVERVIEW.md) | ACTIVE | Philosophy & Pipeline |
| 001 | [CORE_ARCHITECTURE](file:///home/dflory/dev_env/Gravitas/docs/001_core_architecture.md) | ACTIVE | IoC, Drivers, Contracts |
| 002 | [VECTOR_MEMORY](file:///home/dflory/dev_env/Gravitas/docs/002_vector_memory.md) | ACTIVE | Qdrant Hybrid Search |
| 003 | [SECURITY_GATEKEEPER](file:///home/dflory/dev_env/Gravitas/docs/003_security_gatekeeper.md) | ACTIVE | Safety & Escalation |
| 004 | [HARDWARE_OPERATIONS](file:///home/dflory/dev_env/Gravitas/docs/004_hardware_operations.md) | ACTIVE | VRAM & Dual-GPU |
| 005 | [DEVELOPMENT_PROTOCOLS](file:///home/dflory/dev_env/Gravitas/docs/005_development_protocols.md) | ACTIVE | TDD & Retention Cycles |
| 006 | [TELEMETRY_CALIBRATION](file:///home/dflory/dev_env/Gravitas/docs/006_TELEMETRY_CALIBRATION.md) | ACTIVE | Granular Metrics & Phase 4.5 |
