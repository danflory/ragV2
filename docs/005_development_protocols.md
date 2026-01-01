# 005_DEVELOPMENT_PROTOCOLS.md
# STATUS: ACTIVE

## 1. THE ARCHITECT'S OATH (TDD)
We follow a strict **Test-Driven Development (TDD)** loop for all new features:
1.  **Red:** Write a failing test in `tests/`.
2.  **Green:** Write minimal implementation code to pass.
3.  **Refactor:** Clean the code while keeping the test Green.

## 2. THE SOLID STANDARD
1.  **SRP:** Single Responsibility Principle. Modules like `safety.py` and `reflex.py` must stay decoupled.
2.  **IoC:** Inversion of Control. Use `container.py` for all dependency resolution.

## 3. ATOMIC VERSION CONTROL
1.  **Small Commits:** "One feature per commit."
2.  **Auto-Verification:** Run `pytest` and `black` before every commit via the Reflex system.
3.  **Atomic Rollback:** If a change breaks the build, the system reverts immediately to the last known stable state.
