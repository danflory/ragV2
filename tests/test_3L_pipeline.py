import pytest
import os
import sys

# Ensure app is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.L1_local import l1_engine
from app.L2_network import ask_gpt_mini
from app.L3_strategy import ask_gemini_pro

@pytest.mark.asyncio
async def test_L1_local_async_engine():
    """Verifies the new Async Engine communicates with Ollama."""
    print("\n[Pytest] 🐢 Testing Async L1 Engine...")
    
    # We test the engine entry point directly
    response = await l1_engine.ask_local_llm("Say 'L1 Online'")
    
    assert response != "ESCALATE TO L2", "L1 failed and escalated during test."
    assert len(response) > 0, "L1 returned an empty string."
    print(f"   Response received: {response[:30]}...")

@pytest.mark.asyncio
async def test_L2_cloud_reachability():
    """Verifies L2 Cloud API key and connection."""
    response = await ask_gpt_mini("Check connection.")
    assert response is not None
    assert "ESCALATE" not in response

@pytest.mark.asyncio
async def test_L3_strategy_reachability():
    """Verifies L3 Gemini API key and connection."""
    response = await ask_gemini_pro("Check connection.")
    assert response is not None