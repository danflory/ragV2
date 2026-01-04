import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.governance.accountant import accountant
from app.config import config

@pytest.mark.asyncio
async def test_calculate_roi_math():
    """
    Verifies the ROI calculation logic with mock database data.
    """
    # Mock data representing usage_stats rows
    mock_rows = [
        {'layer': 'L1', 'prompt_tokens': 1000, 'completion_tokens': 500, 'duration_ms': 2000}, # Local
        {'layer': 'L2', 'prompt_tokens': 2000, 'completion_tokens': 1000, 'duration_ms': 5000}, # Cloud
    ]

    # Mock the DB pool and fetch
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = mock_rows
    
    # Setup the async with context manager for the pool
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn

    with patch('app.database.db.pool', mock_pool), \
         patch('app.database.db.is_ready', return_value=True):
        
        report = await accountant.calculate_roi()
        
        # Total Tokens: 3000 input, 1500 output
        # Cost If Cloud: (3 * 0.0025) + (1.5 * 0.0100) = 0.0075 + 0.015 = 0.0225
        # L2 Tokens (Cloud): 2000 input, 1000 output
        # L2 Fees: (2 * 0.0025) + (1 * 0.0100) = 0.005 + 0.01 = 0.015
        # Electricity: (7000 / 1000 / 3600) * 0.25 * 0.15 = 0.00194 * 0.25 * 0.15 = 0.0000729
        # Actual Cost: 0.015 + 0.0000729 = ~0.0151
        # Net Savings: 0.0225 - 0.0151 = ~0.0074
        
        assert report['total_input_tokens'] == 3000
        assert report['total_output_tokens'] == 1500
        assert report['cost_if_cloud'] == 0.0225
        assert report['net_savings_usd'] > 0
        assert report['savings_percentage'] > 0
        assert report['audit_status'] == "active"

@pytest.mark.asyncio
async def test_calculate_roi_empty():
    """
    Verifies behavior when no stats are present.
    """
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = []
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn

    with patch('app.database.db.pool', mock_pool), \
         patch('app.database.db.is_ready', return_value=True):
        
        report = await accountant.calculate_roi()
        assert report['net_savings_usd'] == 0
        assert report['savings_percentage'] == 0
