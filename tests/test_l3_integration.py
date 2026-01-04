import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.L3_google import GoogleGeminiDriver
from app.agents.scout import ScoutAgent

@pytest.mark.asyncio
async def test_scout_research_flow():
    """Verifies that ScoutAgent queries memory and calls L3."""
    # 1. Setup Mocks
    mock_l3 = MagicMock()
    mock_l3.generate = AsyncMock(return_value="Synthesized Report")
    
    mock_memory = MagicMock()
    mock_memory.search = AsyncMock(return_value=["Local fact 1", "Local fact 2"])
    
    # 2. Initialize Agent
    agent = ScoutAgent(l3_driver=mock_l3, memory=mock_memory)
    
    # 3. Execute
    report = await agent.research("test query")
    
    # 4. Assertions
    assert report == "Synthesized Report"
    mock_memory.search.assert_called_once_with("test query", top_k=10)
    mock_l3.generate.assert_called_once()
    
    # Verify prompt contains local facts
    call_args = mock_l3.generate.call_args[0][0]
    assert "Local fact 1" in call_args
    assert "Local fact 2" in call_args
    assert "test query" in call_args

@pytest.mark.asyncio
async def test_google_driver_generate():
    """Verifies GoogleGeminiDriver calls the SDK correctly."""
    with patch("app.L3_google.genai.Client") as mock_client_class:
        # Mock the client and its nested structure
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Mock aio.models.generate_content
        mock_response = MagicMock()
        mock_response.text = "Gemini Response"
        
        # This part is tricky because of the aio.models hierarchy
        mock_aio = MagicMock()
        mock_client.aio = mock_aio
        mock_models = MagicMock()
        mock_aio.models = mock_models
        mock_models.generate_content = AsyncMock(return_value=mock_response)
        
        driver = GoogleGeminiDriver(api_key="fake_key", model="gemini-1.5-pro")
        
        # Execute
        result = await driver.generate("Hello")
        
        # Assertions
        assert result == "Gemini Response"
        mock_models.generate_content.assert_called_once()

@pytest.mark.asyncio
async def test_scout_no_context():
    """Verifies Scout handles missing local context gracefully."""
    mock_l3 = MagicMock()
    mock_l3.generate = AsyncMock(return_value="Baseline Report")
    
    mock_memory = MagicMock()
    mock_memory.search = AsyncMock(return_value=[])
    
    agent = ScoutAgent(l3_driver=mock_l3, memory=mock_memory)
    report = await agent.research("rare topic")
    
    assert report == "Baseline Report"
    call_args = mock_l3.generate.call_args[0][0]
    assert "No specific local context found" in call_args
