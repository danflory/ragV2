# 000_MASTER_OVERVIEW.md
# STATUS: ACTIVE
# VERSION: 3.1.0

## 1. CORE PHILOSOPHY
AntiGravity is a **3-Layer Cognitive Pipeline** designed for "Inference Economy"—maximizing local hardware while leveraging cloud IQ for complex reasoning.

*   **L1 (Reflex):** Local, Free, Fast. Runs on Titan RTX (24GB). Handles routine traffic and **Action Reflexes**.
*   **L2 (Reasoning):** Cloud (DeepSeek/Qwen via DeepInfra). High IQ for complex logic and refactoring.
*   **L3 (Deep Research):** Agentic flagship (Gemini 3 Pro). Used for deep document analysis and synthesis.

## 2. THE STACK-FIRST PROTOCOL (Cognitive MVC)
The system operates as a symbiotic relationship between Two Agents:
1.  **The Controller (Local Stack):** Your 3-Level model architecture decides *what* to do.
2.  **The Executor (Developer Agent):** Carrying out the plan via file edits, shell commands, and git syncs.

## 3. CORE DESIGN PRINCIPLES
1.  **SOLID Architecture:** Enforced via `app/container.py` (IoC).
2.  **Test-Driven Development (TDD):** Red-Green-Refactor is the law.
3.  **Reflex Security:** No "hallucinated destruction". All actions pass through the Gatekeeper (`app/safety.py`).
4.  **Hardware Guardrails:** Strict VRAM monitoring (4GB safety floor) to prevent OOM.

## 4. DOCUMENTATION MAP
| ID | Document | Status | Scope |
| :--- | :--- | :--- | :--- |
| 000 | [MASTER_OVERVIEW](file:///home/dflory/dev_env/rag_local/docs/000_MASTER_OVERVIEW.md) | ACTIVE | Philosophy & Pipeline |
| 001 | [CORE_ARCHITECTURE](file:///home/dflory/dev_env/rag_local/docs/001_core_architecture.md) | ACTIVE | IoC, Drivers, Contracts |
| 002 | [VECTOR_MEMORY](file:///home/dflory/dev_env/rag_local/docs/002_vector_memory.md) | ACTIVE | ChromaDB & Retrieval |
| 003 | [SECURITY_GATEKEEPER](file:///home/dflory/dev_env/rag_local/docs/003_security_gatekeeper.md) | DRAFT | Safety & Escalation |
| 004 | [HARDWARE_OPERATIONS](file:///home/dflory/dev_env/rag_local/docs/004_hardware_operations.md) | DRAFT | VRAM & WSL2 |
| 005 | [DEVELOPMENT_PROTOCOLS](file:///home/dflory/dev_env/rag_local/docs/005_development_protocols.md) | DRAFT | TDD & Git Hygiene |
