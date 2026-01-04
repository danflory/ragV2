# 000_MASTER_OVERVIEW.md
# STATUS: ACTIVE
# VERSION: 4.0.0 (Omni-RAG / Dual-GPU)

## 1. CORE PHILOSOPHY
**AntiGravity RAG** is a **Dual-GPU Production-Grade Hybrid RAG Architecture** designed for processing thousands of pages with precision retrieval. The system maximizes "Inference Economy" by cascading requests through three layers of progressive cost and capability.

*   **L1 (Reflex):** Local, Free, Fast. Runs on Titan RTX (24GB). Handles routine traffic and **Action Reflexes**.
*   **L2 (Reasoning):** Cloud (Qwen2.5-Coder-32B via DeepInfra). High IQ for complex logic and refactoring.
*   **L3 (Deep Research):** Agentic flagship (Gemini 3 Pro). Used for deep document analysis and synthesis.

## 2. THE DUAL-GPU ARCHITECTURE
The system leverages **dual NVIDIA GPUs** for parallel processing and implements **Dense + Sparse hybrid vector search** via Qdrant.

*   **GPU 0 (Titan RTX 24GB):** Primary Compute / Generation
*   **GPU 1 (GTX 1060 6GB):** Dedicated Embedding Engine

## 3. CORE DESIGN PRINCIPLES
1.  **SOLID Architecture:** Enforced via `app/container.py` (IoC).
2.  **Test-Driven Development (TDD):** Red-Green-Refactor is the law.
3.  **Reflex Security:** No "hallucinated destruction". All actions pass through the Gatekeeper (`app/safety.py`).
4.  **Hardware Guardrails:** Strict VRAM monitoring with overload protection.

## 4. DOCUMENTATION MAP
| ID | Document | Status | Scope |
| :--- | :--- | :--- | :--- |
| 000 | [MASTER_OVERVIEW](file:///home/dflory/dev_env/rag_local/docs/000_MASTER_OVERVIEW.md) | ACTIVE | Philosophy & Pipeline |
| 001 | [CORE_ARCHITECTURE](file:///home/dflory/dev_env/rag_local/docs/001_core_architecture.md) | ACTIVE | IoC, Drivers, Contracts |
| 002 | [VECTOR_MEMORY](file:///home/dflory/dev_env/rag_local/docs/002_vector_memory.md) | ACTIVE | Qdrant Hybrid Search |
| 003 | [SECURITY_GATEKEEPER](file:///home/dflory/dev_env/rag_local/docs/003_security_gatekeeper.md) | ACTIVE | Safety & Escalation |
| 004 | [HARDWARE_OPERATIONS](file:///home/dflory/dev_env/rag_local/docs/004_hardware_operations.md) | ACTIVE | VRAM & Dual-GPU |
| 005 | [DEVELOPMENT_PROTOCOLS](file:///home/dflory/dev_env/rag_local/docs/005_development_protocols.md) | ACTIVE | TDD & Git Hygiene |
