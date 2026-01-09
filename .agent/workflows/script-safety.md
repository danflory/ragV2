---
description: Mandatory safety protocol for script development and testing.
---

## Protocol: Script Safety Sandbox

Any script (Python, Bash, etc.) created or modified that exceeds **300 characters** must undergo a mandatory testing phase in the safety sandbox.

### 1. The Sandbox Directory
All qualifying scripts must be placed in a dated subdirectory under `temporaryTesting/`:
- **Format**: `temporaryTesting/YYYY-MM-DD/`
- **Example**: `temporaryTesting/2026-01-08/my_script.py`

### 2. Verification Requirement
- Scripts must be executed and verified **within** the sandbox.
- Evidence of successful execution (terminal output, logs) must be captured in the `thoughts.md` journal.

### 3. Promotion to Production
- A script may only be moved to its permanent location (e.g., `scripts/`, `ANTIGRAVITY_Scripts/`) after:
  1. Successful verification in the sandbox.
  2. Explicit user sign-off or completion of a formal `/reason` milestone.

### 4. Git Policy
- The `temporaryTesting/` directory is **locally excluded** from Git via `.git/info/exclude` to prevent accidental inclusion in commits.
