# 005_development_protocols.md
# STATUS: ACTIVE
# VERSION: 6.0.0 (Reasoning Pipes & Wrapper Certification)

## 1. THE ARCHITECT'S OATH (TDD)
We follow a strict **Test-Driven Development (TDD)** loop for all new features:
1.  **Red:** Write a failing test in `tests/`.
2.  **Green:** Write minimal implementation code to pass.
3.  **Refactor:** Clean the code while keeping the test Green.
4.  **Certify:** Agent wrappers MUST pass `WrapperCertifier` validation before being enabled in the Registry.

## 2. THE SOLID STANDARD
1.  **SRP:** Single Responsibility Principle. Modules like `safety.py` and `reflex.py` must stay decoupled.
2.  **IoC:** Inversion of Control. Use `container.py` for all dependency resolution.
3.  **DRY:** Don't Repeat Yourself. Shared functionality centralized in appropriate modules.

## 3. ATOMIC VERSION CONTROL
1.  **Small Commits:** "One feature per commit."
2.  **Auto-Verification:** Run `pytest` and `black` before every commit via the Reflex system.
3.  **Atomic Rollback:** If a change breaks the build, the system reverts immediately to the last known stable state.
4.  **Changelog Maintenance:** Every significant milestone, refactor, or architectural change MUST be documented in `/CHANGELOG.md`.

## 4. ADVANCED DEVELOPMENT PROTOCOLS
* **Dependency Injection:** All system components managed through `container.py` IoC container.
* **Async/Await:** Full asynchronous implementation for performance and scalability.
* **Circuit Breaker Patterns:** Resilient GPU operations with CPU fallbacks.
* **Memory Hygiene:** Automatic pruning of stale vector chunks to prevent rot.
* **Performance Telemetry:** Hardware metrics (Load Latency, Thought Latency, VRAM) are logged to Postgres with a **60-day historic window**. Data is aggregated every 60s to prevent database bloat.
* **Health Monitoring:** Continuous health checks for all microservices.

## 5. REASONING & TRANSPARENCY (The Dual-Track System)
* **Construction Fidelity**: The system construction is managed by the **Antigravity** assistant, ensuring bit-for-bit faithfulness in reasoning logs and action states during the development cycle.
* **Dual-Track Journaling**:
    - **Executive Journal** (`executive.md`): Strategic Crossroads, architectural decisions, and project pulse.
    - **Reasoning Pipe** (`thoughts.md` / `ReasoningPipe_{agentName}.md`): Raw, verbatim internal logic and action states. Use the **Zero-Editing Policy**.
* **Strategic Crossroads**: High-impact decisions must be logged as "Crossroads" at the top of the executive summary (🏁) and require human steering.
* **Retention Cycles**:
    * **Performance Telemetry**: 60 days (Aggregated in Postgres).
    * **Reasoning Pipe Archives**: 14 days (Local files).
    * **Active Buffer**: Cleared and archived on session start (Recon).

## 6. IDENTITY COMPLIANCE
* **Antigravity**: The designation for the external AI Assistant tool used for project construction and orchestration of development tasks.
* **Gravitas**: The designation for the internal RAG system, its core logic, and its departmental specialist agents (e.g., **Gravitas Scout**, **Gravitas Librarian**).

## 7. REASONING PIPE PROTOCOL
All agent wrappers must implement the **Reasoning Pipe** protocol to capture high-fidelity chain-of-thought data.
1.  **Wrapper Certification**: No wrapper can be deployed without passing static and dynamic certification via the `WrapperCertifier`.
2.  **Standardized Journaling**: Logs must be written to `docs/journals/ReasoningPipe_{agent}_{session}.md` in the approved markdown format.
3.  **Supervisor Integration**: Every session must be registered with the `SupervisorGuardian` before execution starts.
4.  **Zero-Editing Policy**: Reasoning logs are raw and immutable. They are the ground truth for system logic.
5.  **Monthly Audits**: All certified agents are subject to monthly quality audits by the `ReasoningPipeAuditor`.


## 8. CODING STANDARDS & BEST PRACTICES
All code must adhere to the standards defined in [CODING_STANDARDS.md](file:///home/dflory/dev_env/Gravitas/docs/CODING_STANDARDS.md):
1.  **Datetime Handling**: Always use timezone-aware datetimes to prevent comparison errors
2.  **Error Handling**: Define custom exception types for domain-specific errors
3.  **Type Hints**: Annotate all public function signatures
4.  **Async/Await**: Properly await all async calls and avoid blocking the event loop
5.  **Pre-Commit Checks**: Run `mypy`, `ruff`, and `black` before committing code
