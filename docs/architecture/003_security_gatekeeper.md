# 003_SECURITY_GATEKEEPER.md
# STATUS: ACTIVE
# VERSION: 4.5.0 (Gravitas Command & Control / Telemetry Calibration)

## 1. THE "TRUST BUT VERIFY" LOOP
To prevent "hallucinated destruction" or secret leakage, all **Reflex Actions** (Shell/Git) must pass through a strict, automated safety filter with multi-format validation.

1.  **Proposal:** L1 or L2 generates an XML reflex tag (Shell, Write, or Git Sync).
2.  **Static Analysis (The Filter - `app/safety.py`):**
    * **Syntax Check:** Multi-format validation (`ast.parse()` for Python, YAML/JSON validators, SQL keyword blocking)
    * **Secret Scanning:** Regex validation prevents committing `.env` keys or high-entropy strings.
    * **Destructive Command Blocklist:** Blocks `rm -rf`, `mkfs`, or modifying protected system files.
    * **Self-Preservation:** Prevents modification of core safety and container files.
3.  **L2 Escalation (The Judge):**
    * If a diff exceeds **50 lines** or touches `core/*.py`, it triggers an asynchronous L2 Review.
    * *Action:* The Reflex is held; L2 approves/rejects; L1 is notified of the verdict.
4.  **Execution:** Only safe, validated actions are executed via `app/reflex.py`.

## 2. GIT HYGIENE & RESILIENCE
* **Pre-Commit Hook (Internal):** The system runs `ruff check` and `black --check` on the proposed file. If it fails, the commit is rejected, and the model is ordered to fix syntax.
* **Atomic Rollback:** If a "Reflex" breaks the build (detected via `pytest` run), the system automatically reverts the last commit.
* **Authentication Resilience:** Graceful handling of Git auth failures in headless containers
* **Tool Resilience:** Cloud CLI detection with Python SDK guidance (`bq`, `gcloud`)

## 3. ADVANCED SECURITY FEATURES
* **Multi-Format Validation:** Python, YAML, JSON, SQL, and Shell syntax checking
* **Scope Restrictions:** Shell commands restricted to `/Gravitas` scope
* **Import Auditing:** Blocks dangerous Python imports (`subprocess`, `os.system`)
* **SQL Protection:** Blocks dangerous SQL keywords (`DROP`, `TRUNCATE`, `DELETE`)
