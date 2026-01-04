# AntiGravity Session Tasks
> **Protocol:** Micro-tasks for the current coding session.
> **Rule:** When a task is complete, mark with [x] and add a brief Result note.

## Phase 18: Omni-RAG Robustness (Current Session)

### 1. Memory Hygiene (The "Vector Rot" Fix)
- [x] **Create Test:** `tests/test_memory_pruning.py` to verify deletion of old chunks before ingestion.
- [x] **Implement:** `prune_source_vectors(source_id)` in `app/memory.py`.
- [x] **Integrate:** Call pruning logic inside `ingest_text` or the ingestor workflow.

### 2. The Gatekeeper (Safety Middleware)
- [x] **Create Test:** `tests/test_safety_logic.py` (Mock dangerous commands and ensure blockage).
- [x] **Implement:** `app/safety.py` with `validate_syntax()` and `scan_secrets()`.
- [x] **Refactor:** Update `app/reflex.py` to import and use `safety.check()` before execution.

### 3. Dual-GPU Resilience
- [x] **Create Test:** `tests/test_embed_breaker.py` (Simulate GPU 1 downtime).
- [x] **Implement:** Add Circuit Breaker to `memory.add_texts` (Fallback to CPU or error gracefully).


### 4. System Telemetry (Infrastructure)
> **Goal:** Build the logging pipeline first so other modules can use it.
- [x] **Schema:** Add `CREATE TABLE system_telemetry` to `app/database.py`.
- [x] **Implement:** Create `app/telemetry.py` with `TelemetryLogger` class (async/non-blocking).
- [x] **Integrate:** Register `telemetry` singleton in `app/container.py`.

### 5. Hardware Safety (Active Defense)
> **Goal:** Use telemetry to protect the hardware.
- [x] **Implement:** Add `check_vram()` to `L1_local.py`.
- [x] **Coordinate:** Inside `check_vram`, call `await telemetry.log("VRAM_CHECK", ...)` to record status.
- [x] **Logic:** If Free VRAM < 2GB:
    - Log event: `await telemetry.log("VRAM_LOCKOUT", ...)`
    - Raise `OverloadError` to stop generation safely.
