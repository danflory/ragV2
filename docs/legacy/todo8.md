Phase 8: The "Scout" (Deep Research)
The Core (L1) and Governance (Accountant) layers are complete. We now integrate the L3 Layer (Google Gemini). Currently, L3_strategy.py exists as a loose script. We will formalize it into The Scout, an agent capable of handling "Deep Research" tasks that require massive context windows (2M+ tokens) or reasoning capabilities beyond the local Titan RTX.

Work Order: Phase 8 (The Scout)

# GRAVITAS WORK ORDER: PHASE 8 (The Scout / L3 Integration)
# STATUS: COMPLETED
# CONTEXT: Integrating Google Gemini (L3) for Deep Research.
# OBJECTIVE: Allow the user to trigger "Deep Research" tasks from the Nexus.

## 1. PRE-FLIGHT
- [x] **Review `app/config.py`:** Ensure `L3_KEY` and `L3_MODEL` ("gemini-1.5-pro" or similar) are set.

## 2. THE DRIVER (Refactor)
- [x] **Refactor `app/L3_strategy.py` -> `app/L3_google.py`:**
    - **Class:** `GoogleGeminiDriver(LLMDriver)`.
    - **Method:** `generate(prompt)`.
    - **Method:** `check_health()`.
    - **Logic:** Use `google.generativeai` SDK.

## 3. THE AGENT (The Scout)
- [x] **Create `app/agents/scout.py`:**
    - **Class:** `ScoutAgent`.
    - **Method:** `research(query: str) -> str`.
    - **Logic:**
        1. Query Qdrant for relevant local context.
        2. Construct a "Deep Research" prompt containing local context + user query.
        3. Send to L3 (Gemini) for synthesis.
        4. Return the comprehensive report.

## 4. THE WIRING (Container & Router)
- [x] **Update `app/container.py`:**
    - Initialize `GoogleGeminiDriver` (L3).
    - Initialize `ScoutAgent` (injecting L3 and Memory).
- [x] **Update `app/router.py`:**
    - Add `POST /agents/scout/research`.
    - Payload: `{"query": "Future of AI hardware"}`.

## 5. THE VIEW (Nexus Dashboard)
- [x] **Update `dashboard/index.html`:**
    - Add "DEEP RESEARCH" card in the Tools pane.
    - Input: "Research Topic".
    - Button: "DEPLOY SCOUT".

## 6. EXIT CRITERIA
- [x] **Run Suite:** `pytest tests/test_l3_integration.py` (Mock the Google API).
- [x] **Submission:** Paste:
    1.  `completed_phase8.md`.
    2.  `app/agents/scout.py`.
    3.  `app/L3_google.py`.