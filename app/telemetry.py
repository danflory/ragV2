import logging
import json
from typing import Any, Dict, Optional
from .database import db

logger = logging.getLogger("AGY_TELEMETRY")

class TelemetryLogger:
    """
    Asynchronous telemetry logger for system events.
    Non-blocking logging to system_telemetry table.
    """

    async def log(
        self,
        event_type: str,
        component: str = None,
        value: float = None,
        metadata: Dict[str, Any] = None,
        status: str = None
    ) -> bool:
        """
        Logs a telemetry event asynchronously.

        Args:
            event_type: Type of event (e.g., "VRAM_CHECK", "VRAM_LOCKOUT")
            component: System component (e.g., "L1", "memory")
            value: Numeric value associated with the event
            metadata: Additional JSON-serializable metadata
            status: Event status (e.g., "OK", "WARNING", "ERROR")

        Returns:
            bool: True if logged successfully, False otherwise
        """
        if not db.is_ready():
            logger.warning("⚠️ TELEMETRY: Database not ready, skipping log")
            return False

        try:
            # Convert metadata dict to JSON string if provided
            metadata_json = json.dumps(metadata) if metadata else None

            async with db.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO system_telemetry (event_type, component, value, metadata, status)
                    VALUES ($1, $2, $3, $4, $5)
                ''', event_type, component, value, metadata_json, status)

            logger.debug(f"📊 TELEMETRY LOGGED: {event_type} ({component or 'unknown'})")
            return True

        except Exception as e:
            logger.error(f"❌ TELEMETRY LOG FAILURE: {e}")
            return False

    async def get_recent_events(self, limit: int = 10, component: str = None) -> list:
        """
        Retrieves recent telemetry events.

        Args:
            limit: Maximum number of events to return
            component: Filter by specific component (optional)

        Returns:
            List of telemetry event dictionaries
        """
        if not db.is_ready():
            return []

        try:
            async with db.pool.acquire() as conn:
                if component:
                    rows = await conn.fetch('''
                        SELECT event_type, component, value, metadata, status, timestamp
                        FROM system_telemetry
                        WHERE component = $1
                        ORDER BY timestamp DESC
                        LIMIT $2
                    ''', component, limit)
                else:
                    rows = await conn.fetch('''
                        SELECT event_type, component, value, metadata, status, timestamp
                        FROM system_telemetry
                        ORDER BY timestamp DESC
                        LIMIT $1
                    ''', limit)

                events = []
                for row in rows:
                    event = dict(row)
                    # Parse metadata JSON back to dict if present
                    if event.get('metadata'):
                        try:
                            event['metadata'] = json.loads(event['metadata'])
                        except:
                            pass  # Keep as string if parsing fails
                    events.append(event)

                return events

        except Exception as e:
            logger.error(f"❌ TELEMETRY QUERY FAILURE: {e}")
            return []

# Singleton Instance
telemetry = TelemetryLogger()
