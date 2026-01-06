"""
Shadow-Audit Loop: Performance tracking and routing decision logging.

Captures every routing decision and actual performance to build a dataset
for future autonomous optimization and cost analysis.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
import uuid
import json

logger = logging.getLogger(__name__)

@dataclass
class TelemetrySnapshot:
    """Snapshot of system telemetry at request time."""
    vram_usage_percent: float
    system_load_percent: float
    avg_latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class RoutingDecision:
    """The routing decision made by the dispatcher."""
    tier: str  # "L1", "L2", or "L3"
    model: str
    reasoning: str
    complexity_estimated: int

@dataclass
class ActualPerformance:
    """Actual performance metrics after request completion."""
    latency_ms: float
    tokens_generated: int
    success: bool
    cost: float
    error: Optional[str] = None

@dataclass
class PerformanceDeviation:
    """Comparison between expected and actual performance."""
    expected_latency_ms: float
    latency_delta_ms: float
    prediction_accuracy_percent: float

@dataclass
class AuditEntry:
    """Complete audit entry for a single request."""
    request_id: str
    timestamp: str
    complexity_estimated: int
    telemetry_snapshot: TelemetrySnapshot
    routing_decision: RoutingDecision
    actual_performance: Optional[ActualPerformance] = None
    deviation: Optional[PerformanceDeviation] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "complexity_estimated": self.complexity_estimated,
            "telemetry_snapshot": asdict(self.telemetry_snapshot),
            "routing_decision": asdict(self.routing_decision),
            "actual_performance": asdict(self.actual_performance) if self.actual_performance else None,
            "deviation": asdict(self.deviation) if self.deviation else None
        }

class ShadowAuditLoop:
    """
    Passive performance tracking system that logs all routing decisions.
    
    This creates a dataset for:
    1. Self-optimization of routing rules
    2. Cost analysis over time
    3. Performance benchmarking
    4. Failure pattern detection
    """
    
    def __init__(self, postgres_client=None):
        """
        Initialize the audit loop.
        
        Args:
            postgres_client: Optional PostgreSQL client for persistence.
                           If None, logs are kept in-memory only.
        """
        self.postgres_client = postgres_client
        self._in_memory_log: Dict[str, AuditEntry] = {}
        self._lock = asyncio.Lock()
    
    async def log_routing_decision(
        self,
        complexity: int,
        telemetry: TelemetrySnapshot,
        routing: RoutingDecision
    ) -> str:
        """
        Log a routing decision when it's made.
        
        Returns:
            request_id: Unique identifier for this request
        """
        request_id = str(uuid.uuid4())
        
        entry = AuditEntry(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat(),
            complexity_estimated=complexity,
            telemetry_snapshot=telemetry,
            routing_decision=routing
        )
        
        async with self._lock:
            self._in_memory_log[request_id] = entry
        
        logger.info(f"[AUDIT] Request {request_id[:8]} routed to {routing.tier}/{routing.model}")
        
        # Persist to database if available
        if self.postgres_client:
            await self._persist_to_db(entry)
        
        return request_id
    
    async def log_actual_performance(
        self,
        request_id: str,
        performance: ActualPerformance
    ):
        """
        Log actual performance after request completion.
        
        Calculates deviation from expected performance.
        """
        async with self._lock:
            entry = self._in_memory_log.get(request_id)
            if not entry:
                logger.warning(f"[AUDIT] Unknown request_id: {request_id}")
                return
            
            entry.actual_performance = performance
            
            # Calculate deviation
            expected_latency = entry.telemetry_snapshot.avg_latency_ms
            latency_delta = performance.latency_ms - expected_latency
            
            # Avoid division by zero
            if expected_latency > 0:
                accuracy = 100.0 * (1 - abs(latency_delta) / expected_latency)
            else:
                accuracy = 100.0 if latency_delta == 0 else 0.0
            
            entry.deviation = PerformanceDeviation(
                expected_latency_ms=expected_latency,
                latency_delta_ms=latency_delta,
                prediction_accuracy_percent=max(0.0, accuracy)
            )
        
        logger.info(
            f"[AUDIT] Request {request_id[:8]} completed: "
            f"{performance.latency_ms:.1f}ms, "
            f"{performance.tokens_generated} tokens, "
            f"${performance.cost:.4f}"
        )
        
        # Update database
        if self.postgres_client:
            await self._update_db(entry)
    
    async def get_entry(self, request_id: str) -> Optional[AuditEntry]:
        """Retrieve a specific audit entry."""
        async with self._lock:
            return self._in_memory_log.get(request_id)
    
    async def get_recent_entries(self, limit: int = 100) -> list[AuditEntry]:
        """Get the most recent audit entries."""
        async with self._lock:
            entries = sorted(
                self._in_memory_log.values(),
                key=lambda e: e.timestamp,
                reverse=True
            )
            return entries[:limit]
    
    async def get_tier_statistics(self, tier: str) -> Dict[str, Any]:
        """
        Calculate statistics for a specific tier.
        
        Returns:
            - total_requests: Number of requests routed to this tier
            - avg_latency_ms: Average latency
            - total_cost: Total cost
            - success_rate: Percentage of successful requests
        """
        async with self._lock:
            tier_entries = [
                e for e in self._in_memory_log.values()
                if e.routing_decision.tier == tier and e.actual_performance
            ]
        
        if not tier_entries:
            return {
                "total_requests": 0,
                "avg_latency_ms": 0.0,
                "total_cost": 0.0,
                "success_rate": 0.0
            }
        
        total_requests = len(tier_entries)
        latencies = [e.actual_performance.latency_ms for e in tier_entries]
        costs = [e.actual_performance.cost for e in tier_entries]
        successes = [e.actual_performance.success for e in tier_entries]
        
        return {
            "total_requests": total_requests,
            "avg_latency_ms": sum(latencies) / total_requests,
            "total_cost": sum(costs),
            "success_rate": (sum(successes) / total_requests) * 100.0
        }
    
    async def _persist_to_db(self, entry: AuditEntry):
        """Persist audit entry to PostgreSQL."""
        if not self.postgres_client:
            return
        
        try:
            query = """
                INSERT INTO routing_audit (
                    request_id, timestamp, complexity_estimated,
                    telemetry_snapshot, routing_decision
                ) VALUES ($1, $2, $3, $4, $5)
            """
            await self.postgres_client.execute(
                query,
                entry.request_id,
                entry.timestamp,
                entry.complexity_estimated,
                json.dumps(asdict(entry.telemetry_snapshot)),
                json.dumps(asdict(entry.routing_decision))
            )
        except Exception as e:
            logger.error(f"[AUDIT] Failed to persist to DB: {e}")
    
    async def _update_db(self, entry: AuditEntry):
        """Update audit entry with actual performance."""
        if not self.postgres_client or not entry.actual_performance:
            return
        
        try:
            query = """
                UPDATE routing_audit
                SET actual_performance = $1, deviation = $2
                WHERE request_id = $3
            """
            await self.postgres_client.execute(
                query,
                json.dumps(asdict(entry.actual_performance)),
                json.dumps(asdict(entry.deviation)) if entry.deviation else None,
                entry.request_id
            )
        except Exception as e:
            logger.error(f"[AUDIT] Failed to update DB: {e}")
    
    async def cleanup_old_entries(self, days: int = 60):
        """
        Remove audit entries older than the specified number of days.
        
        Aligns with the 60-day telemetry retention policy.
        """
        cutoff = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
        
        async with self._lock:
            self._in_memory_log = {
                rid: entry for rid, entry in self._in_memory_log.items()
                if entry.timestamp >= cutoff_iso
            }
        
        # Database cleanup
        if self.postgres_client:
            try:
                query = "DELETE FROM routing_audit WHERE timestamp < $1"
                await self.postgres_client.execute(query, cutoff_iso)
                logger.info(f"[AUDIT] Cleaned up entries older than {days} days")
            except Exception as e:
                logger.error(f"[AUDIT] Cleanup failed: {e}")

# Global instance
_audit_loop: Optional[ShadowAuditLoop] = None

def get_audit_loop() -> ShadowAuditLoop:
    """Get or create the global audit loop instance."""
    global _audit_loop
    if _audit_loop is None:
        _audit_loop = ShadowAuditLoop()
    return _audit_loop
