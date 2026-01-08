"""
Gravitas Telemetry Service - Main FastAPI Application
Standalone microservice for telemetry event ingestion and querying.
"""
import logging
import asyncio
import json
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import List, Optional

from app.services.telemetry.models import (
    TelemetryEvent,
    TelemetryEventResponse,
    TelemetryQuery,
    TelemetryEventRecord,
    TelemetryStatsResponse,
    HealthResponse
)
from app.services.telemetry.database import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Gravitas_TELEMETRY_SERVICE")

# Background queue for batching writes
event_queue: asyncio.Queue = asyncio.Queue(maxsize=10000)
worker_task: Optional[asyncio.Task] = None


async def telemetry_worker():
    """
    Background worker that batches telemetry events for efficient writes.
    Processes events from queue and writes to database.
    """
    logger.info("📊 Telemetry worker started")
    batch_size = 50
    batch_timeout = 2.0  # seconds
    
    while True:
        try:
            batch = []
            deadline = asyncio.get_event_loop().time() + batch_timeout
            
            # Collect events until batch size or timeout
            while len(batch) < batch_size:
                timeout = max(0.1, deadline - asyncio.get_event_loop().time())
                try:
                    event = await asyncio.wait_for(event_queue.get(), timeout=timeout)
                    if event is None:  # Shutdown signal
                        logger.info("📊 Telemetry worker received shutdown signal")
                        # Process remaining batch before shutdown
                        if batch:
                            await _write_batch(batch)
                        return
                    batch.append(event)
                except asyncio.TimeoutError:
                    break
            
            # Write batch if we have events
            if batch:
                await _write_batch(batch)
                
        except Exception as e:
            logger.error(f"❌ Telemetry worker error: {e}")
            await asyncio.sleep(1)  # Brief pause before retry


async def _write_batch(batch: List[TelemetryEvent]):
    """Write a batch of events to the database."""
    if not db.is_ready():
        logger.warning(f"⚠️ Database not ready, dropping {len(batch)} events")
        return
    
    try:
        async with db.pool.acquire() as conn:
            # Prepare batch insert
            values = [
                (
                    event.event_type,
                    event.component,
                    event.value,
                    json.dumps(event.metadata) if event.metadata else None,
                    event.status
                )
                for event in batch
            ]
            
            await conn.executemany('''
                INSERT INTO system_telemetry (event_type, component, value, metadata, status)
                VALUES ($1, $2, $3, $4, $5)
            ''', values)
            
            logger.debug(f"✅ Wrote batch of {len(batch)} telemetry events")
            
    except Exception as e:
        logger.error(f"❌ Batch write failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global worker_task
    
    # Startup
    logger.info("📊 Telemetry Service starting up...")
    try:
        await db.connect()
        await db.init_schema()
        logger.info("✅ Database connected and schema initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Start background worker
    worker_task = asyncio.create_task(telemetry_worker())
    logger.info("✅ Background telemetry worker started")
    
    yield
    
    # Shutdown
    logger.info("📊 Telemetry Service shutting down...")
    
    # Stop worker and flush queue
    if worker_task:
        await event_queue.put(None)  # Shutdown signal
        await worker_task
    
    await db.disconnect()
    logger.info("🛑 Telemetry Service shutdown complete")


app = FastAPI(
    title="Gravitas Telemetry Service",
    description="Dedicated microservice for telemetry event ingestion and observability.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "telemetry",
        "database": db.is_ready(),
        "queue_depth": event_queue.qsize()
    }


@app.post("/v1/telemetry/log", response_model=TelemetryEventResponse)
async def log_event(event: TelemetryEvent):
    """
    Log a telemetry event (fire-and-forget).
    Events are queued and batch-written to database.
    """
    try:
        # Non-blocking queue add
        event_queue.put_nowait(event)
        return {
            "success": True,
            "message": "Event queued for processing"
        }
    except asyncio.QueueFull:
        logger.error("❌ Telemetry queue full, dropping event")
        raise HTTPException(status_code=503, detail="Telemetry queue full")


@app.get("/v1/telemetry/events", response_model=List[TelemetryEventRecord])
async def get_events(
    limit: int = 10,
    component: Optional[str] = None,
    event_type: Optional[str] = None,
    hours: Optional[int] = None
):
    """
    Retrieve recent telemetry events with optional filtering.
    """
    if not db.is_ready():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        async with db.pool.acquire() as conn:
            # Build query with filters
            query = "SELECT * FROM system_telemetry WHERE 1=1"
            params = []
            param_count = 0
            
            if component:
                param_count += 1
                query += f" AND component = ${param_count}"
                params.append(component)
            
            if event_type:
                param_count += 1
                query += f" AND event_type = ${param_count}"
                params.append(event_type)
            
            if hours:
                param_count += 1
                query += f" AND timestamp > NOW() - INTERVAL '{hours} hours'"
            
            param_count += 1
            query += f" ORDER BY timestamp DESC LIMIT ${param_count}"
            params.append(limit)
            
            rows = await conn.fetch(query, *params)
            
            # Convert to response models
            events = []
            for row in rows:
                event_dict = dict(row)
                # Parse JSON metadata
                if event_dict.get('metadata'):
                    try:
                        event_dict['metadata'] = json.loads(event_dict['metadata'])
                    except:
                        pass
                events.append(TelemetryEventRecord(**event_dict))
            
            return events
            
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise HTTPException(status_code=500, detail="Query execution failed")


@app.get("/v1/telemetry/stats", response_model=TelemetryStatsResponse)
async def get_stats(
    component: Optional[str] = None,
    hours: int = 24
):
    """
    Get aggregated statistics for telemetry events.
    """
    if not db.is_ready():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        async with db.pool.acquire() as conn:
            query = '''
                SELECT 
                    component,
                    COUNT(*) as measurement_count,
                    AVG(value) as avg_efficiency_score,
                    MIN(value) as best_efficiency,
                    MAX(value) as worst_efficiency,
                    COALESCE(SUM((metadata->>'tokens_generated')::int), 0) as total_tokens
                FROM system_telemetry
                WHERE event_type = 'THOUGHT_LATENCY'
                    AND timestamp > NOW() - INTERVAL '%s hours'
            '''
            
            if component:
                query += " AND component = $1 GROUP BY component"
                row = await conn.fetchrow(query % hours, component)
            else:
                query += " GROUP BY component LIMIT 1"
                row = await conn.fetchrow(query % hours)
            
            if not row:
                return TelemetryStatsResponse(
                    component=component,
                    measurement_count=0,
                    avg_efficiency_score=None,
                    best_efficiency=None,
                    worst_efficiency=None,
                    total_tokens=None,
                    time_window_hours=hours
                )
            
            return TelemetryStatsResponse(
                **dict(row),
                time_window_hours=hours
            )
            
    except Exception as e:
        logger.error(f"❌ Stats query failed: {e}")
        raise HTTPException(status_code=500, detail="Stats query failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
