import asyncio
import os
import sys
import pytest
from unittest.mock import patch, AsyncMock

# Setup Import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.L1_local import l1_engine

async def test_resilience():
    print("🧨 Starting L1 API Resilience Test...\n")

    # --- TEST 1: API Connection Verification ---
    print("--- TEST 1: Verifying Ollama Service Connection ---")
    is_ready = await l1_engine.check_model_exists()
    if is_ready:
        print("✅ PASS: Ollama is running and model is present.")
    else:
        print("❌ FAIL: Ollama service is unreachable or model is missing.")

    # --- TEST 2: Graceful Escalation on Failure ---
    print("\n--- TEST 2: Simulating API Failure (Should trigger Escalation) ---")
    with patch("ollama.AsyncClient.generate", side_effect=Exception("Simulated GPU Crash")):
        response = await l1_engine.ask_local_llm("This should fail")
        if response == "ESCALATE TO L2":
            print("✅ PASS: Driver correctly caught exception and requested Escalation.")
        else:
            print(f"❌ FAIL: Driver did not return Escalation string. Got: {response}")

if __name__ == "__main__":
    asyncio.run(test_resilience())