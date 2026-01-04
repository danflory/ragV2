import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from app.container import container
from app.config import config
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_container_switch_mode():
    """Verify that switching mode updates container state and driver."""
    # Mock the L1 driver's load_model to avoid real network calls
    with patch.object(container.l1_driver, 'load_model', new_callable=AsyncMock) as mock_load:
        mock_load.return_value = True
        
        # Reset to default for testing reproducibility
        container.current_mode = config.DEFAULT_MODE
        
        # Switch to DEV mode
        success = await container.switch_mode("dev")
        
        assert success is True
        assert container.current_mode == "dev"
        mock_load.assert_called_with(config.MODEL_MAP["dev"])
        
        # Switch back to RAG mode
        success = await container.switch_mode("rag")
        assert success is True
        assert container.current_mode == "rag"
        mock_load.assert_called_with(config.MODEL_MAP["rag"])

@pytest.mark.asyncio
async def test_router_mode_endpoint():
    """Verify the API endpoint calls the container switch logic."""
    # Patch the container's switch_mode method
    with patch.object(container, 'switch_mode', new_callable=AsyncMock) as mock_switch:
        mock_switch.return_value = True
        
        # We need to use the actual client but mock the internal logic
        response = client.post("/system/mode", json={"mode": "dev"})
        
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "dev" in response.json()["message"]
        mock_switch.assert_called_with("dev")

@pytest.mark.asyncio
async def test_invalid_mode():
    """Verify that switching to an invalid mode fails."""
    # Reset to a known mode
    container.current_mode = "rag"
    
    success = await container.switch_mode("non_existent_mode")
    assert success is False
    assert container.current_mode == "rag" # Should not change
