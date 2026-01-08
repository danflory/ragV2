import time
import logging
import asyncio
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
from app.services.gatekeeper.database import db

logger = logging.getLogger("Gravitas_AUDIT_LOG")

@dataclass
class AuditEvent:
    action: str
    resource: str
    ghost_id: str
    shell_id: Optional[str] = None
    result: str = "PENDING"
    reason: Optional[str] = None
    metadata: Optional[Dict] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class AuditLogger:
    """
    Records security-relevant events to the database and system logs.
    Uses an internal queue and background worker to prevent blocking requests.
    """
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.queue = asyncio.Queue()
        self._worker_task = None
        self._loop = None

    def _start_worker(self):
        """Starts the background worker if not already running."""
        try:
            loop = asyncio.get_running_loop()
            if self._worker_task is None or self._worker_task.done():
                self._worker_task = loop.create_task(self._worker())
                self._loop = loop
                logger.info("🚀 Audit background worker started.")
        except RuntimeError:
            # No running loop, will start on log_event
            pass

    async def log_event(self, event: AuditEvent):
        """Logs an event by adding it to the queue (non-blocking)."""
        if not self.enabled:
            return

        # 1. Log to system logs immediately (minimal overhead)
        log_msg = f"AUDIT: [{event.result}] Ghost:{event.ghost_id} Action:{event.action} Resource:{event.resource}"
        if event.reason:
            log_msg += f" Reason:{event.reason}"
        logger.info(log_msg)

        # 2. Add to queue for DB persistence
        self._start_worker()
        self.queue.put_nowait(event)

    async def _worker(self):
        """Background worker that persists events to DB."""
        logger.info("👷 Audit worker processing queue...")
        while True:
            event = await self.queue.get()
            try:
                await self._persist_to_db(event)
            except Exception as e:
                logger.error(f"Error in audit worker: {e}")
            finally:
                self.queue.task_done()

    async def _persist_to_db(self, event: AuditEvent):
        """Internal method to perform the actual DB write."""
        try:
            if not db.is_ready():
                await db.connect()
            
            async with db.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO audit_log (
                        timestamp, ghost_id, shell_id, action, resource, result, reason, metadata
                    ) VALUES (
                        to_timestamp($1), $2, $3, $4, $5, $6, $7, $8
                    )
                ''', 
                event.timestamp,
                event.ghost_id,
                event.shell_id,
                event.action,
                event.resource,
                event.result,
                event.reason,
                str(event.metadata) if event.metadata else None
                )
        except Exception as e:
            logger.error(f"Failed to write to audit_log table: {e}")

    async def flush(self):
        """Waits for all pending events in the queue to be processed."""
        if self.queue.empty():
            return
        logger.info(f"⏳ Flushing {self.queue.qsize()} audit events...")
        await self.queue.join()
        logger.info("✅ Audit buffer flushed.")

    async def stop(self):
        """Stops the worker and flushes the queue."""
        if self._worker_task:
            await self.flush()
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            logger.info("🛑 Audit worker stopped.")

    async def query_events(self, ghost_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Retrieves recent audit events."""
        try:
            if not db.is_ready():
                await db.connect()
            
            query = "SELECT * FROM audit_log"
            args = []
            if ghost_id:
                query += " WHERE ghost_id = $1"
                args.append(ghost_id)
            
            query += " ORDER BY timestamp DESC LIMIT " + str(limit)
            
            async with db.pool.acquire() as conn:
                rows = await conn.fetch(query, *args)
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to query audit_log: {e}")
            return []

# Singleton instance
audit_logger = AuditLogger()
