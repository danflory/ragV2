# 003_SECURITY_GATEKEEPER.md
# STATUS: ACTIVE
# VERSION: 7.1.0 (The Security Tier)

## 1. THE SECURITY TRIAD
Security in Gravitas is enforced by three distinct entities, ensuring separation of duties.

### 1.1 The Gatekeeper Service (The Enforcer)
*   **Port:** `8001` / `8002`
*   **Role:** Validates **Authorizations** (Can you do this?) and **Actions** (Is this safe?).
*   **Mechanism:**
    *   **JWT Validation:** Checks signature and expiration.
    *   **Policy Engine:** Enforces `access_policies.yaml` (e.g., "Scout cannot Delete").
    *   **Safety Filter:** Uses `app/safety.py` to statically analyze payloads for malicious code (RM-RF, SQL Injection).

### 1.2 The Guardian Service (The Authority)
*   **Port:** `8003`
*   **Role:** Issues and Validates **Identities** (Who are you?).
*   **Mechanism:**
    *   **Certificate Authority:** Signs x509-style certificates for Wrappers.
    *   **Ledger:** Maintains a database of valid/revoked certificates.
    *   **Badge System:** Maps `GhostID` to `ShellID` to `Capabilities`.

### 1.3 The Supervisor (The Orchestrator)
*   **Port:** `8000`
*   **Role:** Ensures the workflow is followed.
*   **Mechanism:** It blindly routes requests but **First** asks Guardian "Is this agent valid?" and Gatekeeper "Is this action allowed?".

## 2. THE "TRUST BUT VERIFY" LOOP
1.  **Request:** Shell proposes a Tool Call (e.g., `write_file`).
2.  **Intercept:** Supervisor pauses execution.
3.  **Validate:** Supervisor calls `Gatekeeper.validate(payload)`.
    *   Gatekeeper runs `app/safety.py` static analysis.
    *   Gatekeeper checks Policy DB.
4.  **Verdict:**
    *   **200 OK:** Supervisor executes tool.
    *   **403 FORBIDDEN:** Supervisor returns error to Shell (Reflex rejection).
    *   **401 UNAUTHORIZED:** Audit Log Event triggered.

## 3. ADVANCED SAFETY FEATURES (Inside Gatekeeper)
*   **Multi-Format Validation:** Python, YAML, JSON, SQL, and Shell syntax checking.
*   **Secret Scanning:** Regex validation prevents committing `.env` keys.
*   **Destructive Blocklist:** Blocks `rm -rf`, `mkfs`.
*   **Import Auditing:** Blocks dangerous Python imports (`subprocess`, `os.system`).

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
