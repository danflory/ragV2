# GRAVITAS WORK ORDER: PHASE 4.2 (Hardware State Machine)
# STATUS: QUEUED
# CONTEXT: Managing VRAM constraints on Titan RTX (24GB).
# OBJECTIVE: Implement Mutually Exclusive Modes (RAG_MODE vs. DEV_MODE).

## 1. PRE-FLIGHT (Configuration)
- [x] **Update `app/config.py`:**
    - Define constants: `MODE_RAG = "rag"` (gemma2:27b), `MODE_DEV = "dev"` (deepseek-coder-v2).
    - Add `DEFAULT_MODE` setting.

## 2. THE DRIVER LAYER (L1 Updates)
- [x] **Update `app/interfaces.py`:**
    - Add `load_model(model_name: str)` to the `LLMDriver` abstract base class.
- [x] **Refactor `app/L1_local.py`:**
    - Implement `load_model` in `LocalLlamaDriver`.
    - **Logic:** Should call `ensure_model()` (pull/load) for the new target and update `self.model_name`.

## 3. THE SWITCHBOARD (State Management)
- [x] **Update `app/container.py`:**
    - Add `current_mode` property.
    - Implement `switch_mode(target_mode: str) -> bool`.
    - **Logic:**
        1. Check if `target_mode` differs from current.
        2. Resolve model name from config.
        3. Call `l1_driver.load_model(new_model)`.
        4. Update `current_mode`.

## 4. THE API (Control Surface)
- [x] **Update `app/router.py`:**
    - Add `POST /system/mode` endpoint.
    - **Payload:** `{"mode": "dev"}` or `{"mode": "rag"}`.
    - Returns success/fail status.

## 5. VERIFICATION (TDD)
- [x] **Create `tests/test_mode_switching.py`:**
    - Mock the Ollama API calls (don't actually wait 2 mins for loading).
    - Verify `container.switch_mode` updates the driver's model name.
    - Verify `router` calls the switch correctly.

## 6. EXIT CRITERIA
- [x] **Run Suite:** `pytest tests/test_mode_switching.py` (PASS).
- [x] **Receipt:** Append results to `completed_phase4.2.md`.