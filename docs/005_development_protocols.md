# 005_development_protocols.md
# STATUS: ACTIVE
# VERSION: 4.0.0 (Gravitas Grounded Research / Dual-GPU)

## 1. THE ARCHITECT'S OATH (TDD)
We follow a strict **Test-Driven Development (TDD)** loop for all new features:
1.  **Red:** Write a failing test in `tests/`.
2.  **Green:** Write minimal implementation code to pass.
3.  **Refactor:** Clean the code while keeping the test Green.

## 2. THE SOLID STANDARD
1.  **SRP:** Single Responsibility Principle. Modules like `safety.py` and `reflex.py` must stay decoupled.
2.  **IoC:** Inversion of Control. Use `container.py` for all dependency resolution.
3.  **DRY:** Don't Repeat Yourself. Shared functionality centralized in appropriate modules.

## 3. ATOMIC VERSION CONTROL
1.  **Small Commits:** "One feature per commit."
2.  **Auto-Verification:** Run `pytest` and `black` before every commit via the Reflex system.
3.  **Atomic Rollback:** If a change breaks the build, the system reverts immediately to the last known stable state.
4.  **Changelog Maintenance:** Every significant milestone, refactor, or architectural change MUST be documented in `/CHANGELOG.md` following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## 4. ADVANCED DEVELOPMENT PROTOCOLS
* **Dependency Injection:** All system components managed through `container.py` IoC container
* **Async/Await:** Full asynchronous implementation for performance and scalability
* **Circuit Breaker Patterns:** Resilient GPU operations with CPU fallbacks
* **Memory Hygiene:** Automatic pruning of stale vector chunks to prevent rot
* **Telemetry Logging:** Comprehensive system event logging to Postgres
* **Health Monitoring:** Continuous health checks for all microservices

## 5. REASONING & TRANSPARENCY
* **Developer Journal**: All AI-driven architectural decisions must be mirrored in dated files within `docs/journals/`.
* **Thinking Transparency**: The forensic `thoughts.md` log is maintained specifically to help humans understand the agent's internal reasoning process, with tool-failure auditing as a secondary benefit.
* **Strategic Crossroads**: High-impact decisions (Speed vs. Stability, Cost vs. Quality) must be logged as "Crossroads" and require human approval.
* **Transient Context**: Documents like `GRAVITAS_SESSION_CONTEXT.md` are ephemeral and refreshed on every system boot.
