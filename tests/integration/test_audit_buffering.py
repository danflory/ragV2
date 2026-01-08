import pytest
import asyncio
import time
from app.services.gatekeeper.audit import AuditLogger, AuditEvent
from app.services.gatekeeper.database import db

@pytest.mark.asyncio
async def test_audit_buffering_latency():
    """
    TDD Test: Verify that logging an event does not block for more than 5ms,
    even if the database write is slow.
    """
    # 1. Setup - Mock a slow database insert by wrapping the current pool or just observing
    # For now, we measure the baseline. The current implementation awaits db.pool.acquire()
    
    logger = AuditLogger(enabled=True)
    event = AuditEvent(
        action="test_action",
        resource="test_resource",
        ghost_id="test_ghost"
    )
    
    start_time = time.perf_counter()
    await logger.log_event(event)
    end_time = time.perf_counter()
    
    duration_ms = (end_time - start_time) * 1000
    
    # Ideally, with buffering, this should be < 1ms (just a queue put)
    # The current sync-await implementation will likely take > 5ms depending on DB environment
    print(f"Audit log duration: {duration_ms:.4f}ms")
    assert duration_ms < 5.0, f"Logging took too long: {duration_ms:.2f}ms. Should be non-blocking."

@pytest.mark.asyncio
async def test_audit_buffering_persistence():
    """
    Verify that even if log_event returns immediately, the event eventually lands in DB.
    """
    logger = AuditLogger(enabled=True)
    event = AuditEvent(
        action="persistence_test",
        resource="res_1",
        ghost_id="ghost_1",
        metadata={"test": "buffered"}
    )
    
    await logger.log_event(event)
    
    # Wait for background task to process (if implemented)
    await asyncio.sleep(0.5)
    
    # Query back
    events = await logger.query_events(ghost_id="ghost_1")
    assert any(e['action'] == "persistence_test" for e in events)

@pytest.mark.asyncio
async def test_audit_buffering_shutdown_flush():
    """
    Verify that the buffer is flushed on shutdown.
    """
    # This will be tested once the lifespan integration is planned
    pass
