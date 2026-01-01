### TODO: Standardize Agentic Action Protocol
* **Priority:** Medium (Tech Debt)
* **Context:** Currently, L1 uses a magic token `<<GIT_SYNC>>` while L2 uses XML `<reflex>`.
* **Goal:** Refactor L1 system prompt and `L1_local.py` to output/parse `<reflex action="git_sync">`.
* **Benefit:** Enables a single, unified parser in `router.py` (DRY Principle).