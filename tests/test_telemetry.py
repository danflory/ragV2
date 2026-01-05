"""
Test Suite: Telemetry Logger
Tests system telemetry logging and querying functionality
"""
import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock, AsyncMock

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.telemetry import TelemetryLogger

class TestTelemetryLogger:
    """Test telemetry logging functionality."""

    @pytest.fixture
    def telemetry_logger(self):
        """Create a fresh TelemetryLogger instance for each test."""
        return TelemetryLogger()

    @pytest.mark.asyncio
    async def test_log_event_success(self, telemetry_logger):
        """Test successful logging of a telemetry event."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True
            mock_conn = AsyncMock()
            
            # Setup async context manager for db.pool.acquire()
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value = mock_conn
            mock_db.pool.acquire.return_value = mock_cm

            # Log an event
            result = await telemetry_logger.log(
                event_type="VRAM_CHECK",
                component="L1",
                value=4096.0,
                metadata={"gpu_id": 0},
                status="OK"
            )

            assert result is True
            mock_conn.execute.assert_called_once()
            call_args = mock_conn.execute.call_args[0]
            assert "INSERT INTO system_telemetry" in call_args[0]
            # Check arguments (excluding the SQL string at index 0)
            assert call_args[1:] == ("VRAM_CHECK", "L1", 4096.0, '{"gpu_id": 0}', "OK")

    @pytest.mark.asyncio
    async def test_log_event_database_not_ready(self, telemetry_logger):
        """Test logging when database is not ready."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = False

            with patch('app.telemetry.logger') as mock_logger:
                result = await telemetry_logger.log("TEST_EVENT")

                assert result is False
                mock_logger.warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_log_event_database_error(self, telemetry_logger):
        """Test handling of database errors during logging."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True

            # Setup failing async context manager
            mock_cm = AsyncMock()
            mock_cm.__aenter__.side_effect = Exception("DB Error")
            mock_db.pool.acquire.return_value = mock_cm

            with patch('app.telemetry.logger') as mock_logger:
                result = await telemetry_logger.log("TEST_EVENT")

                assert result is False
                mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_log_event_minimal_params(self, telemetry_logger):
        """Test logging with only required event_type parameter."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True
            mock_conn = AsyncMock()
            
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value = mock_conn
            mock_db.pool.acquire.return_value = mock_cm

            result = await telemetry_logger.log("MINIMAL_EVENT")

            assert result is True
            call_args = mock_conn.execute.call_args[0]
            assert call_args[1:] == ("MINIMAL_EVENT", None, None, None, None)

    @pytest.mark.asyncio
    async def test_get_recent_events_all(self, telemetry_logger):
        """Test retrieving recent events without component filter."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True
            mock_conn = AsyncMock()
            
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value = mock_conn
            mock_db.pool.acquire.return_value = mock_cm

            # Mock database response
            mock_row = MagicMock()
            mock_row.__getitem__.side_effect = lambda key: {
                'event_type': 'VRAM_CHECK',
                'component': 'L1',
                'value': 4096.0,
                'metadata': '{"gpu_id": 0}',
                'status': 'OK',
                'timestamp': '2024-01-01T12:00:00Z'
            }.get(key)
            mock_row.keys.return_value = ['event_type', 'component', 'value', 'metadata', 'status', 'timestamp']
            mock_conn.fetch.return_value = [mock_row]

            events = await telemetry_logger.get_recent_events(limit=5)

            assert len(events) == 1
            event = events[0]
            assert event['event_type'] == 'VRAM_CHECK'
            assert event['component'] == 'L1'
            assert event['value'] == 4096.0
            assert event['metadata'] == {"gpu_id": 0}
            assert event['status'] == 'OK'

            # Verify query without component filter
            call_args = mock_conn.fetch.call_args[0]
            assert "WHERE component" not in call_args[0]
            assert call_args[1:] == (5,)

    @pytest.mark.asyncio
    async def test_get_recent_events_filtered(self, telemetry_logger):
        """Test retrieving recent events with component filter."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True
            mock_conn = AsyncMock()
            
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value = mock_conn
            mock_db.pool.acquire.return_value = mock_cm

            mock_conn.fetch.return_value = []

            events = await telemetry_logger.get_recent_events(limit=10, component="L1")

            assert events == []
            call_args = mock_conn.fetch.call_args[0]
            assert "WHERE component = $1" in call_args[0]
            assert call_args[1:] == ("L1", 10)

    @pytest.mark.asyncio
    async def test_get_recent_events_database_not_ready(self, telemetry_logger):
        """Test querying when database is not ready."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = False

            events = await telemetry_logger.get_recent_events()

            assert events == []

    @pytest.mark.asyncio
    async def test_get_recent_events_query_error(self, telemetry_logger):
        """Test handling of query errors."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True

            mock_cm = AsyncMock()
            mock_cm.__aenter__.side_effect = Exception("Query Error")
            mock_db.pool.acquire.return_value = mock_cm

            with patch('app.telemetry.logger') as mock_logger:
                events = await telemetry_logger.get_recent_events()

                assert events == []
                mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_recent_events_malformed_metadata(self, telemetry_logger):
        """Test handling of malformed JSON metadata."""
        with patch('app.telemetry.db') as mock_db:
            mock_db.is_ready.return_value = True
            mock_conn = AsyncMock()
            
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value = mock_conn
            mock_db.pool.acquire.return_value = mock_cm

            # Mock row with malformed JSON metadata
            mock_row = MagicMock()
            mock_row.__getitem__.side_effect = lambda key: {
                'event_type': 'TEST_EVENT',
                'component': 'TEST',
                'value': None,
                'metadata': '{"invalid": json}',
                'status': None,
                'timestamp': '2024-01-01T12:00:00Z'
            }.get(key)
            mock_row.keys.return_value = ['event_type', 'component', 'value', 'metadata', 'status', 'timestamp']
            mock_conn.fetch.return_value = [mock_row]

            events = await telemetry_logger.get_recent_events(limit=1)

            assert len(events) == 1
            assert events[0]['metadata'] == '{"invalid": json}'

if __name__ == "__main__":
    pytest.main([__file__])
