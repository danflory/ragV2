# TODO 6.0 DEBT REPAYMENT PLAN (Flash Execution)

> **Instruction for Agent:** This file is optimized for high-speed execution. Pick an item, execute it, mark it [x], and move to the next.

## 1. Security Hygiene (High Urgency)
- [x] **Scan for Secrets:** Run grep checks for common API key patterns (`sk-`, `ghp_`) in the codebase.
    - *Target:* `app/` and `scripts/`
    - *Action:* Verified clean (only hits in `safety.py`).

## 2. Stability Hardening (Medium Urgency)
- [x] **Global Exception Handler:** Review `app/storage.py` (MinIO) and `app/memory.py` (Qdrant) for generic exception catching.
    - *Action:* Updated `app/storage.py` to catch `minio.error.S3Error`. `app/memory.py` generic handling deemed sufficient for now.
    - *Goal:* Ensure the system degrades gracefully if a container is offline.

## 3. Environment Standardization (Low Urgency)
- [x] **VENV Check:** Ensure `requirements.txt` is strictly pinned for core dependencies.
    - *Action:* Audited `fastapi`, `minio`, `pydantic`. All match `requirements.txt` exactly.

---
*Generated: 2026-01-06 based on ROADMAP.md Backlog*
