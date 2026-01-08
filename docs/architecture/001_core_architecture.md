# 001_CORE_ARCHITECTURE.md
# STATUS: ACTIVE
# VERSION: 7.1.0 (Microservices & Drivers)

## 1. THE SERVICE MESH (The "body")
The system is composed of localized microservices that communicate via HTTP/REST (and eventually gRPC).

### 1.1 The Operational Flow
1.  **Lobby (UI):** User sends a request.
2.  **Supervisor (Orchestrator):** Receives request, determines intent.
3.  **Gatekeeper (Security):** Validates JWT and Policy `POST /gatekeeper/validate`.
4.  **Guardian (Identity):** Verifies Agent Certificate `GET /guardian/validate`.
5.  **Router (Traffic):** Dispatches to the appropriate Model Driver `POST /v1/chat/completions`.

## 2. THE DRIVER PATTERN (The "Hands")
*Used inside the `gravitas_router` service.*
The Router connects to **Shells** (LLM Runtimes) via **Drivers**. These adapters translate internal requests into vendor-specific API calls.

### 2.1 Driver Types
*   **Type A (Local L1):** `LocalLlamaDriver`. Config-injected. Targeted at Ollama/Titan RTX.
*   **Type B (Cloud L2):** `DeepInfraDriver`. Key-injected. Targeted at Specialized Models.
*   **Type C (Research L3):** `GeminiDriver`. targeted at Frontier Models (Gemini 2.0 Flash / Pro).

## 3. THE CONTAINER (The "Switchboard")
*   **File:** `app/container.py`
*   **Role:** **Inversion of Control (IoC) Root**.
*   **Usage:** Each microservice instantiates its own `Container` to manage internal dependencies (Database connections, Logging, Telemetry).
*   **Rule:** Business logic **MUST NEVER** instantiate drivers or infrastructure directly. It must request them from the `container`.

## 4. THE REFLEX LOOP (The "Nervous System")
*   **Rule:** Actions (Tool Calls) are proposed by the Shell, but executed by the Supervisor.
*   **Flow:** Shell (Thought) -> Supervisor (Catch) -> Gatekeeper (Check Policy) -> Tool Execution.
*   **Safety:** `app/safety.py` provides the static analysis engine used by the Gatekeeper service to scan for dangerous syntax, secrets, and destructive commands.

