# Phase 6.5: The Conceptual Shift

**Status**: ✅ CORE COMPLETE (2026-01-06)  
**Summary**: See `EXECUTION_SUMMARY.md` for full details.

## 1. Registry & Identity (The "Ghost" Layer)
- [x] Create `app/services/registry/ghost_registry.py` (Defines Librarian, Scout, etc.).
- [x] Rename `app/services/registry/agent_registry.py` to `shell_registry.py`.
- [x] Create backward compatibility facade in `agent_registry.py`.
- [ ] Update `app/container.py` to instantiate Ghosts instead of raw Drivers (Deferred to Phase 7).

## 2. Database Schema (Memory)
- [x] Create `scripts/migrations/001_add_identity_columns.sql`.
- [x] Execute migration: Add `ghost_id` and `shell_id` to `history` table.
- [x] Backfill 98 historical records with "legacy_ghost" / "legacy_shell".
- [x] Update `app/database.py` to write these new fields.
- [x] Update `app/database.py` to read these new fields.
- [ ] Make columns NON-NULL (Deferred until all write paths verified).

## 3. Infrastructure (Lobby vs. Supervisor)
- [x] Rename service `rag_app` to `gravitas_lobby` in `docker-compose.yml`.
- [ ] Refactor `app/router.py` -> `app/services/lobby/intercom.py` (Deferred to Phase 7).
- [ ] Move "ESCALATE" logic from Router to `GravitasSupervisor` (Dispatcher) (Deferred to Phase 7).

## 4. Operational Alignment
- [x] Update `ReasoningPipe` to use `Ghost.name` for journal filenames.
- [ ] Audit and move `scripts/` tools to `app/agents/{Agent}/tools/` (Deferred to Phase 7).
