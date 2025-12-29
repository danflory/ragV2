import pytest
from unittest.mock import patch, AsyncMock
from app.router import chat_endpoint, ChatRequest
from app.config import config

@pytest.mark.asyncio
async def test_router_escalation_flow():
    """
    Ensures that if L1 fails (returns 'ESCALATE TO L2'),
    the router passes that signal up to the caller.
    """
    # FIX: Patch the NEW path via the container
    # app.router -> container -> l1_driver -> generate
    with patch("app.router.container.l1_driver.generate", new_callable=AsyncMock) as mock_generate:
        # Simulate L1 Failure
        mock_generate.return_value = "ESCALATE TO L2"
        
        request = ChatRequest(message="Hello")
        response = await chat_endpoint(request)
        
        assert response["response"] == "ESCALATE TO L2"
        mock_generate.assert_called_once()

@pytest.mark.asyncio
async def test_vram_guard_trigger():
    """
    Ensures the VRAM guard correctly blocks the 16B model
    when resources are low.
    """
    # Force config to the heavy model for this test
    config.MODEL = "deepseek-coder-v2:16b"
    
    # Patch the VRAM check function
    with patch("app.router.check_vram_headroom", return_value=False) as mock_vram:
        
        request = ChatRequest(message="Crash me")
        response = await chat_endpoint(request)
        
        # Should block and return escalation
        assert "ESCALATE TO L2" in response["response"]
        assert "(VRAM Limit)" in response["response"]
    
    # Reset config for other tests
    config.MODEL = "codellama:7b"