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
    """
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    async def log_event(self, event: AuditEvent):
        """Logs an event asynchronously."""
        if not self.enabled:
            return

        # 1. Log to system logs immediately
        log_msg = f"AUDIT: [{event.result}] Ghost:{event.ghost_id} Action:{event.action} Resource:{event.resource}"
        if event.reason:
            log_msg += f" Reason:{event.reason}"
        logger.info(log_msg)

        # 2. Log to Database
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
            # We don't raise here to avoid breaking the application flow on logging failure

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
