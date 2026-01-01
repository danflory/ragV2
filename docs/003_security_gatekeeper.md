# 003_SECURITY_GATEKEEPER.md
# STATUS: ACTIVE
# SCOPE: Action Validation & Safety

## 1. THE "TRUST BUT VERIFY" LOOP
To prevent "hallucinated destruction" or secret leakage, all **Reflex Actions** (Shell/Git) must pass through a strict, automated safety filter.

1.  **Proposal:** L1 or L2 generates an XML reflex tag (Shell, Write, or Git Sync).
2.  **Static Analysis (The Filter - `app/safety.py`):**
    * **Syntax Check:** `ast.parse()` ensures generated Python is valid.
    * **Secret Scanning:** Regex validation prevents committing `.env` keys or high-entropy strings.
    * **Destructive Command Blocklist:** Blocks `rm -rf`, `mkfs`, or modifying `.git` internals.
3.  **L2 Escalation (The Judge):**
    * If a diff exceeds **50 lines** or touches `core/*.py`, it triggers an asynchronous L2 Review.
    * *Action:* The Reflex is held; L2 approves/rejects; L1 is notified of the verdict.
4.  **Execution:** Only safe, validated actions are executed via `app/reflex.py`.

## 2. GIT HYGIENE
* **Pre-Commit Hook (Internal):** The system runs `ruff check` and `black --check` on the proposed file. If it fails, the commit is rejected, and the model is ordered to fix syntax.
* **Atomic Rollback:** If a "Reflex" breaks the build (detected via `pytest` run), the system automatically reverts the last commit.
