# Gravitas Grounded Research - Nomenclature & Standards

This document defines the naming conventions for the Gravitas project to ensure consistency across documentation, code, and infrastructure.

## 1. THE CORE BRAND
- **Project Name:** Gravitas Grounded Research
- **Short Name:** Gravitas
- **Project Construction:** Antigravity (External AI Assistant)
- **Legacy Name:** AntiGravity (AGY) - *Deprecated & Removed*

## 2. INFRASTRUCTURE & CONTAINERS
| Category | Standard Name | Port | Role |
| :--- | :--- | :--- | :--- |
| **Backend** | `Gravitas_mcp` | 5050 | FastAPI / Python Logic |
| **L1 Model** | `Gravitas_ollama` | 11434 | local LLM (Titan RTX) |
| **Embeddings** | `Gravitas_ollama_embed` | 11435 | Embeddings (GTX 1060) |
| **Vector DB** | `Gravitas_qdrant` | 6333 | Hybrid Memory Store |
| **Storage** | `Gravitas_minio` | 9000 | Raw Document Blobs |
| **Database** | `postgres_db` | 5432 | History & Telemetry |

## 3. CODE IDENTIFIERS
- **Loggers:** `Gravitas_LAYERNAME` (e.g. `Gravitas_L1`, `Gravitas_ROUTER`)
- **Environment Prefixes:** `Gravitas_` (e.g. `Gravitas_API_KEY`)
- **Database User:** `Gravitas_user`
- **Database Pass:** `Gravitas_pass`

## 4. DESIGNATION HIERARCHY
- **L1:** Reflex Layer (Local Hardware)
- **L2:** Reasoning Layer (Cloud API / DeepInfra)
- **L3:** Agentic Layer (Deep Research / Google Gemini 3)

## 5. REFACTORING RULES
When renaming or creating new components:
1. Always prefix with `Gravitas_` if it's a globally accessible service.
2. Maintain camelCase or snake_case as per the existing file standard (snake_case for Python, camelCase for JS).
3. Update the `GRAVITAS_SESSION_CONTEXT.md` after any major naming changes.
