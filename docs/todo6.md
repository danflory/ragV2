# GRAVITAS WORK ORDER: PHASE 6 (Governance & Grounding)
# STATUS: DONE
# CONTEXT: Implementing Cost Tracking (Accountant) and Quality Control (Inspector).
# OBJECTIVE: Prove the "Inference Economy" ROI and enforce TDD receipts.

## 1. PRE-FLIGHT (Configuration)
- [x] **Update `app/config.py`:**
    - Add Pricing Constants for "Cloud Equivalents" (e.g., GPT-4o rates) to calculate savings.
        - `REF_COST_INPUT_1K = 0.0025` (e.g., $2.50/1M)
        - `REF_COST_OUTPUT_1K = 0.0100` (e.g., $10.00/1M)
    - Add `GRAVITAS_COST_KWH = 0.15` (Local Electricity cost estimate).

## 2. THE ACCOUNTANT (Value Tracking)
- [x] **Create `app/governance/` directory.**
- [x] **Create `app/governance/accountant.py`:**
    - **Class:** `CostAccountant`.
    - **Method:** `calculate_roi()`.
    - **Logic:**
        1. Query `usage_stats` table from Postgres.
        2. Sum Total Tokens (Local L1 vs Cloud L2).
        3. Calculate `Cost_If_Cloud` (Tokens * Ref_Rate).
        4. Calculate `Actual_Cost` (L2 Fees + Est. Electricity).
        5. Return `net_savings_usd` and `savings_percentage`.
- [x] **Test:** `tests/test_accountant.py` (Mock DB rows and verify math).

## 3. THE INSPECTOR (Quality Control)
- [x] **Create `app/governance/inspector.py`:**
    - **Class:** `QualityInspector`.
    - **Method:** `audit_receipt(file_path)`.
    - **Logic:**
        1. Parse a `completed_*.md` file.
        2. **FAIL** if "TEST RESULTS" section is missing.
        3. **FAIL** if logs contain "FAILED" or "ERROR".
        4. **PASS** only if clean test logs are found.
- [x] **Test:** `tests/test_inspector.py` (Feed valid/invalid markdown receipts).

## 4. THE API (Reporting)
- [x] **Update `app/router.py`:**
    - Add `GET /governance/financials`.
    - Returns JSON: `{ "total_savings": 150.50, "roi_percent": 98.5, "audit_status": "active" }`.

## 5. THE VIEW (Nexus Dashboard)
- [x] **Update `dashboard/index.html`:**
    - Add a **"Financials" Card** (Green text for savings).
    - Display "Net Savings" and "ROI".
- [x] **Update `dashboard/app.js`:**
    - Poll `/governance/financials` and update the HUD.

## 6. EXIT CRITERIA
- [x] **Run Suite:** `pytest tests/test_accountant.py tests/test_inspector.py`.
- [x] **Submission:** Paste:
    1.  `completed_phase6.md` (Receipt).
    2.  `app/governance/accountant.py`.
    3.  `dashboard/index.html` (Updated).