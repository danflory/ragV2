# COMPLETED PHASE 4.2: HARDWARE STATE MACHINE

## Objective achieved
Implemented mutually exclusive modes (RAG vs DEV) to manage VRAM constraints on Titan RTX.

## Changes:
1.  **app/config.py**: Defined `MODE_RAG`, `MODE_DEV`, `DEFAULT_MODE`, and `MODEL_MAP`.
2.  **app/interfaces.py**: Added `load_model(model_name: str)` to `LLMDriver` interface.
3.  **app/L1_local.py**: Implemented `load_model` in `LocalLlamaDriver`.
4.  **app/L2_network.py**: Implemented `load_model` in `DeepInfraDriver` (no-op/model update).
5.  **app/container.py**: Added `current_mode` and `switch_mode` logic.
6.  **app/router.py**: Added `POST /system/mode` endpoint and improved health endpoint.
7.  **tests/test_mode_switching.py**: Added TDD suite for verification.

## Test Results:
```
============================== test session starts ===============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0 -- /home/dflory/dev_env/rag_local/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/dflory/dev_env
configfile: pyproject.toml
plugins: anyio-4.12.0, asyncio-1.3.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

tests/test_mode_switching.py ...                                         [100%]

========================= 3 passed, 4 warnings in 12.37s =========================
```

## Readiness:
System is now capable of hot-swapping between `gemma2:27b` (RAG) and `deepseek-coder-v2` (DEV) via API.
