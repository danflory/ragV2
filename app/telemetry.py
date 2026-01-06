import logging
import json
import time
from typing import Any, Dict, Optional
from .database import db

logger = logging.getLogger("Gravitas_TELEMETRY")

class TelemetryLogger:
    """
    Asynchronous telemetry logger for system events.
    Non-blocking logging to system_telemetry table with sub-second precision.
    
    Supports:
    - Load Latency: VRAM model loading time tracking
    - Thought Latency: Inference speed tracking  
    - Token-aware efficiency metrics
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
    
    async def log_load_latency(
        self, 
        model_name: str, 
        load_time_seconds: float,
        success: bool = True
    ) -> bool:
        """
        Logs VRAM model load latency with sub-second precision.
        
        Args:
            model_name: Name of the model being loaded
            load_time_seconds: Time taken to load in seconds (float for precision)
            success: Whether the load succeeded
            
        Returns:
            bool: True if logged successfully
        """
        return await self.log(
            event_type="LOAD_LATENCY",
            component=model_name,
            value=load_time_seconds,
            metadata={"model": model_name, "load_time_ms": round(load_time_seconds * 1000, 2)},
            status="OK" if success else "ERROR"
        )
    
    async def log_thought_latency(
        self,
        model_name: str,
        inference_time_seconds: float,
        tokens_generated: int,
        prompt_tokens: int = 0
    ) -> bool:
        """
        Logs inference latency with token-aware efficiency metrics.
        
        Args:
            model_name: Name of the model used for inference
            inference_time_seconds: Time taken for inference (float for precision)
            tokens_generated: Number of tokens generated
            prompt_tokens: Number of tokens in the prompt
            
        Returns:
            bool: True if logged successfully
        """
        # Calculate efficiency score: Latency-Per-Token (ms/token)
        efficiency_score = (inference_time_seconds * 1000) / tokens_generated if tokens_generated > 0 else 0
        
        return await self.log(
            event_type="THOUGHT_LATENCY",
            component=model_name,
            value=efficiency_score,  # Store efficiency score as primary value
            metadata={
                "model": model_name,
                "inference_time_ms": round(inference_time_seconds * 1000, 2),
                "tokens_generated": tokens_generated,
                "prompt_tokens": prompt_tokens,
                "total_tokens": tokens_generated + prompt_tokens,
                "latency_per_token_ms": round(efficiency_score, 4)
            },
            status="OK"
        )
    
    @staticmethod
    def start_timer() -> float:
        """Returns current time for latency measurement."""
        return time.perf_counter()
    
    @staticmethod
    def measure_latency(start_time: float) -> float:
        """
        Calculates latency from start_time to now.
        
        Args:
            start_time: Result from start_timer()
            
        Returns:
            float: Elapsed time in seconds
        """
        return time.perf_counter() - start_time
    
    async def get_aggregated_efficiency(
        self,
        component: str = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        Calculates aggregated efficiency metrics over a time window.
        
        Args:
            component: Filter by model/component name (optional)
            hours: Time window in hours (default 24)
            
        Returns:
            Dict with weighted efficiency scores and statistics
        """
        if not db.is_ready():
            return {}
        
        try:
            async with db.pool.acquire() as conn:
                query = '''
                    SELECT 
                        component,
                        COUNT(*) as measurement_count,
                        AVG(value) as avg_efficiency_score,
                        MIN(value) as best_efficiency,
                        MAX(value) as worst_efficiency,
                        SUM((metadata->>'tokens_generated')::int) as total_tokens
                    FROM system_telemetry
                    WHERE event_type = 'THOUGHT_LATENCY'
                        AND timestamp > NOW() - INTERVAL '%s hours'
                '''
                
                if component:
                    query += " AND component = $1 GROUP BY component"
                    row = await conn.fetchrow(query % hours, component)
                else:
                    query += " GROUP BY component"
                    rows = await conn.fetch(query % hours)
                    
                    # Return aggregated data for all components
                    if rows:
                        return {
                            "components": [dict(row) for row in rows],
                            "time_window_hours": hours
                        }
                    return {}
                
                if row:
                    return dict(row)
                return {}
                    
        except Exception as e:
            logger.error(f"❌ AGGREGATION QUERY FAILURE: {e}")
            return {}
    
    async def get_60day_statistics(self) -> Dict[str, Any]:
        """
        Retrieves 60-day historic performance window statistics.
        
        Returns:
            Dict with long-term performance trends
        """
        if not db.is_ready():
            return {}
        
        try:
            async with db.pool.acquire() as conn:
                # Get overall statistics
                overall = await conn.fetchrow('''
                    SELECT 
                        COUNT(*) as total_measurements,
                        COUNT(DISTINCT component) as unique_models,
                        MIN(timestamp) as oldest_record,
                        MAX(timestamp) as newest_record
                    FROM system_telemetry
                    WHERE timestamp > NOW() - INTERVAL '60 days'
                ''')
                
                # Get per-model efficiency trends
                trends = await conn.fetch('''
                    SELECT 
                        component,
                        AVG(value) as avg_efficiency,
                        COUNT(*) as measurement_count,
                        SUM((metadata->>'total_tokens')::int) as total_tokens_processed
                    FROM system_telemetry
                    WHERE event_type = 'THOUGHT_LATENCY'
                        AND timestamp > NOW() - INTERVAL '60 days'
                    GROUP BY component
                    ORDER BY avg_efficiency ASC
                ''')
                
                return {
                    "overall": dict(overall) if overall else {},
                    "model_trends": [dict(row) for row in trends] if trends else [],
                    "retention_window_days": 60
                }
                
        except Exception as e:
            logger.error(f"❌ 60-DAY STATISTICS FAILURE: {e}")
            return {}
    
    async def get_telemetry_footprint(self) -> Dict[str, Any]:
        """
        Monitors the telemetry database footprint to prevent bloat.
        
        Returns:
            Dict with table sizes, row counts, and storage metrics
        """
        if not db.is_ready():
            return {}
        
        try:
            async with db.pool.acquire() as conn:
                # Get table size statistics
                table_stats = await conn.fetch('''
                    SELECT 
                        schemaname,
                        tablename,
                        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
                        pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
                    FROM pg_tables
                    WHERE schemaname = 'public'
                        AND tablename IN ('system_telemetry', 'usage_stats', 'history')
                    ORDER BY size_bytes DESC
                ''')
                
                # Get row counts
                telemetry_count = await conn.fetchval('SELECT COUNT(*) FROM system_telemetry')
                usage_count = await conn.fetchval('SELECT COUNT(*) FROM usage_stats')
                history_count = await conn.fetchval('SELECT COUNT(*) FROM history')
                
                # Get oldest records
                oldest_telemetry = await conn.fetchval('SELECT MIN(timestamp) FROM system_telemetry')
                
                return {
                    "table_sizes": [dict(row) for row in table_stats] if table_stats else [],
                    "row_counts": {
                        "system_telemetry": telemetry_count,
                        "usage_stats": usage_count,
                        "history": history_count
                    },
                    "oldest_telemetry_record": str(oldest_telemetry) if oldest_telemetry else None,
                    "monitored_at": str(time.time())
                }
                
        except Exception as e:
            logger.error(f"❌ FOOTPRINT MONITORING FAILURE: {e}")
            return {}

# Singleton Instance
telemetry = TelemetryLogger()
