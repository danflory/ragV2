# GRAVITAS WORK ORDER: PHASE 5 (The Nexus Dashboard)
# STATUS: COMPLETED
# CONTEXT: Connecting the Frontend to the v4.0 API.

## 1. PRE-FLIGHT
- [x] **Review `dashboard/`:** Existing files (`index.html`, `app.js`) are legacy and likely disconnected.

## 2. THE CONTROLLER (Logic)
- [x] **Refactor `dashboard/app.js`:**
    - Implement polling for `GET /health/detailed` (Visual GPU Status).
    - Implement polling for `GET /stats/summary` (Token Counters).
    - **Add Action:** `toggleSystemMode(targetMode)` -> Calls `POST /system/mode`.
    - **Add Action:** `triggerIngest()` -> Calls `POST /ingest`.

## 3. THE VIEW (UI)
- [x] **Update `dashboard/index.html`:**
    - Add **"Mode Toggle" Switch** (RAG vs DEV).
    - Add **"Ingest Knowledge" Button**.
    - Add **Live VRAM Indicators** (using data from health check).
    - Ensure it uses the dark/sci-fi aesthetic defined in `style.css`.

## 4. VERIFICATION (Manual)
- [x] **Launch:** Open `http://localhost:5050/dashboard/` (requires mounting static files in `main.py` if not already present).
- [x] **Test:** Click "Switch to Dev Mode" -> Verify VRAM changes via `nvidia-smi` or logs.

## 5. EXIT CRITERIA
- [x] **Submission:** Paste:
    1.  `completed_phase5.md` (Screenshot description or confirmation).
    2.  `dashboard/app.js`.
    3.  `dashboard/index.html`.
    