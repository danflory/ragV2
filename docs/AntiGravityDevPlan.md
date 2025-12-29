AntiGravity Development Plan
Phase 1: Core Server & Routing
• Server Entry: Create `app/main.py` to initialize FastAPI.

• L3 Logic: Update `app/router.py` to support "Reasoning Mode" (Gemini Pro).

• L3 Testing: Verify `test_l3.py` with valid API Key.

Phase 2: Knowledge & Memory
• Ingestion Script: Create script to parse `docs/` and load into ChromaDB.

• Memory Controls: Add "Clear History" functionality to API.

Phase 3: Interface
• UI Integration: Set up Open WebUI or VS Code extension to talk to Port 5050.

• Testing: End-to-end test of L1 (Local) -> L2 (Cloud) -> L3 (Reasoning) pipeline.
