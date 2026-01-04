import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.exceptions import OverloadError
from app.L1_local import LocalLlamaDriver
from app.config import Settings

class MockGPU:
    def __init__(self, id, memoryTotal, memoryUsed, memoryFree):
        self.id = id
        self.memoryTotal = memoryTotal
        self.memoryUsed = memoryUsed
        self.memoryFree = memoryFree

@pytest.fixture
def mock_config():
    config = Mock(spec=Settings)
    config.L1_URL = "http://localhost:11434"
    config.L1_MODEL = "test-model"
    return config

@pytest.fixture
def l1_driver(mock_config):
    return LocalLlamaDriver(mock_config)

@pytest.mark.asyncio
async def test_vram_check_normal_conditions(l1_driver):
    """Test VRAM check under normal conditions (should pass)"""
    # Mock GPUtil to return normal VRAM usage
    mock_gpu = MockGPU(id=0, memoryTotal=24576, memoryUsed=10240, memoryFree=14336)  # 24GB total, 14GB free
    
    with patch('GPUtil.getGPUs', return_value=[mock_gpu]):
        with patch('app.L1_local.telemetry.log', new_callable=AsyncMock) as mock_telemetry:
            result = await l1_driver.check_vram()
            
            # Should return VRAM info without raising exception
            assert len(result) == 1
            assert result[0]['free_gb'] == 14.0
            assert result[0]['total_gb'] == 24.0
            
            # Should log VRAM check
            mock_telemetry.assert_called_with(
                event_type="VRAM_CHECK",
                component="L1",
                value=14.0,
                metadata={'gpu_id': 0, 'total_vram_gb': 24.0, 'used_vram_gb': 10.0},
                status="OK"
            )

@pytest.mark.asyncio
async def test_vram_check_overload_condition(l1_driver):
    """Test VRAM check when free memory is below threshold (should raise OverloadError)"""
    # Mock GPUtil to return low VRAM usage
    mock_gpu = MockGPU(id=0, memoryTotal=24576, memoryUsed=23552, memoryFree=1024)  # 24GB total, 1GB free
    
    with patch('GPUtil.getGPUs', return_value=[mock_gpu]):
        with patch('app.L1_local.telemetry.log', new_callable=AsyncMock) as mock_telemetry:
            # Should raise OverloadError
            with pytest.raises(OverloadError) as exc_info:
                await l1_driver.check_vram()
            
            # Check exception details
            assert "VRAM overload detected" in str(exc_info.value)
            assert exc_info.value.resource_type == "VRAM"
            assert exc_info.value.current_value == 1.0
            assert exc_info.value.threshold == 2.0
            
            # Should log both VRAM check and lockout
            assert mock_telemetry.call_count == 2
            mock_telemetry.assert_any_call(
                event_type="VRAM_CHECK",
                component="L1",
                value=1.0,
                metadata={'gpu_id': 0, 'total_vram_gb': 24.0, 'used_vram_gb': 23.0},
                status="OK"
            )
            mock_telemetry.assert_any_call(
                event_type="VRAM_LOCKOUT",
                component="L1",
                value=1.0,
                metadata={'gpu_id': 0, 'total_vram_gb': 24.0, 'used_vram_gb': 23.0},
                status="ERROR"
            )

@pytest.mark.asyncio
async def test_vram_check_multiple_gpus(l1_driver):
    """Test VRAM check with multiple GPUs"""
    # Mock GPUtil to return multiple GPUs
    mock_gpus = [
        MockGPU(id=0, memoryTotal=24576, memoryUsed=10240, memoryFree=14336),  # 14GB free
        MockGPU(id=1, memoryTotal=6144, memoryUsed=5120, memoryFree=1024)     # 1GB free (overload)
    ]
    
    with patch('GPUtil.getGPUs', return_value=mock_gpus):
        with patch('app.L1_local.telemetry.log', new_callable=AsyncMock):
            # Should raise OverloadError due to second GPU
            with pytest.raises(OverloadError) as exc_info:
                await l1_driver.check_vram()
            
            assert "VRAM overload detected on GPU 1" in str(exc_info.value)

@pytest.mark.asyncio
async def test_vram_check_monitoring_failure(l1_driver):
    """Test VRAM check when monitoring fails (should continue without raising)"""
    with patch('GPUtil.getGPUs', side_effect=Exception("GPU monitoring failed")):
        with patch('app.L1_local.logger.error') as mock_logger:
            result = await l1_driver.check_vram()
            
            # Should return empty list and log error, but not raise exception
            assert result == []
            mock_logger.assert_called_with("❌ VRAM CHECK FAILED: GPU monitoring failed")

@pytest.mark.asyncio
async def test_generate_calls_vram_check(l1_driver):
    """Test that generate method calls VRAM check before generation"""
    with patch.object(l1_driver, 'check_vram', new_callable=AsyncMock) as mock_check_vram:
        with patch('httpx.AsyncClient') as mock_client:
            # Mock the HTTP client response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "test response"}
            mock_client_instance = Mock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_client_instance
            
            # Call generate
            result = await l1_driver.generate("test prompt")
            
            # Should call VRAM check
            mock_check_vram.assert_called_once()
            
            # Should return response
            assert result == "test response"
