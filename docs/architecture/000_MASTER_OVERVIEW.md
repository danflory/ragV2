# 000_MASTER_OVERVIEW.md
# STATUS: ACTIVE
# VERSION: 7.1.0 (Gravitas Microservices & Security Tier)

## 1. CORE PHILOSOPHY
**Gravitas Grounded Research** is a **Microservices-Based Agentic Architecture**. It separates **Identity** (Ghosts), **Execution** (Shells), **Governance** (Supervisor), and **Security** (Gatekeeper/Guardian) into distinct, resilient services. The internal system orchestration, logic, and departmental specialists (the "Workers") all operate under the **Gravitas** namespace.

## 2. THE GRAVITAS META-MODEL
*The Physics of the World.*

| Concept | Gravitas Primitive | Definition |
| :--- | :--- | :--- |
| **Identity** | **Ghost** | The permanent role (e.g., The Librarian). |
| **Brain** | **Shell** | The interchangeable runtime model (e.g., gemma2). |
| **Object** | **Artifact** | Passive data with value (Books, Journals). |
| **Space** | **Context Scope** | **Public:** Lobby (Ephemeral). **Private:** Room (Persistent). |

## 3. THE MICROSERVICES ARCHITECTURE (RFC-001)
The system is decomposed into specialized tiers:

1.  **Lobby (5050):** PUBLIC. User Interface and Session Management.
2.  **Supervisor (8000):** PRIVATE. Orchestration and Routing.
3.  **Gatekeeper (8001/8002):** PRIVATE. Security Policy and Audit Logging.
4.  **Guardian (8003):** PRIVATE. Identity Certification and Badge Management.
5.  **Router (8005):** PRIVATE. Traffic dispatch to L1/L2/L3 Models.

## 4. THE DUAL-GPU HARDWARE LAYER
*   **GPU 0 (Titan RTX 24GB):** Primary Compute (L1 Models).
*   **GPU 1 (GTX 1060 6GB):** Embedding Engine.

## 5. CORE DESIGN PRINCIPLES
1.  **Thinking Transparency:** Bit-for-bit faithfulness in reasoning logs via Reasoning Pipes.
2.  **Zero-Trust Security:** Every action requires a Valid Certificate (Guardian) and Policy Approval (Gatekeeper).
3.  **Inversion of Control:** Dependencies managed via `app/container.py`.
4.  **Test-Driven Development:** Red-Green-Refactor.
5.  **Inference Economy:** Cost-optimized routing.

## 6. DOCUMENTATION MAP
| ID | Document | Status | Scope |
| :--- | :--- | :--- | :--- |
| 000 | [MASTER_OVERVIEW](file:///home/dflory/dev_env/Gravitas/docs/architecture/000_MASTER_OVERVIEW.md) | **v7.1** | Philosophy & Pipeline |
| 001 | [CORE_ARCHITECTURE](file:///home/dflory/dev_env/Gravitas/docs/architecture/001_core_architecture.md) | **v7.1** | Services, Drivers, IoC |
| 002 | [VECTOR_MEMORY](file:///home/dflory/dev_env/Gravitas/docs/architecture/002_vector_memory.md) | **v4.5** | Qdrant Hybrid Search |
| 003 | [SECURITY_GATEKEEPER](file:///home/dflory/dev_env/Gravitas/docs/architecture/003_security_gatekeeper.md) | **v7.1** | Gatekeeper & Safety |
| 004 | [HARDWARE_OPERATIONS](file:///home/dflory/dev_env/Gravitas/docs/architecture/004_hardware_operations.md) | **v4.5** | VRAM & Dual-GPU |
| 005 | [DEVELOPMENT_PROTOCOLS](file:///home/dflory/dev_env/Gravitas/docs/development/005_development_protocols.md) | **v6.0** | TDD & Retention Cycles |
| 007 | [MODEL_GOVERNANCE](file:///home/dflory/dev_env/Gravitas/docs/architecture/007_model_governance.md) | **v7.0** | Certification & Wrappers |
| 008 | [REASONING_PIPES](file:///home/dflory/dev_env/Gravitas/docs/architecture/008_reasoning_pipes.md) | **v7.0** | Thinking Transparency |

