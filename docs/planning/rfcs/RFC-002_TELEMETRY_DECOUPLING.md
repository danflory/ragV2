# RFC-002: Telemetry & Observability Decoupling

| Metadata | Value |
| :--- | :--- |
| **RFC ID** | RFC-002 |
| **Status** | PROPOSED |
| **Created** | 2026-01-08 |
| **Author** | Antigravity |
| **Topic** | Microservices Architecture |

## 1. Summary
Extract the current in-process telemetry logic (`app/telemetry.py`) into a standalone microservice (`gravitas-telemetry`). Replace the current SQL-executing module with a lightweight HTTP client SDK.

## 2. Motivation
Currently, `app/telemetry.py` is tightly coupled to `app/database.py` and the PostgreSQL instance. This creates two critical issues for the microservices architecture (Phase 7):
1.  **Dependency Leak**: Services like `L1_local` or the new `Router` must have full database connectivity and credentials just to log checks or usage stats.
2.  **Performance Blocking**: Direct DB writes within the critical path of inference (e.g., in `LocalLlamaDriver`) can introduce latency if the DB is under load.

## 3. Proposed Design

### 3.1 New Service: `gravitas-telemetry`
A dedicated FastAPI service running on a new port (e.g., 8002).
- **Responsibilities**:
    - Ingest logs/metrics via HTTP API.
    - Batch write to `system_telemetry` and `usage_stats` tables.
    - Manage table schemas for telemetry.
    - Provide query endpoints for dashboards.

### 3.2 API Interface
```json
POST /v1/telemetry/log
{
  "event_type": "VRAM_CHECK",
  "component": "L1",
  "value": 12.5,
  "metadata": { ... },
  "status": "OK"
}
```

### 3.3 Client SDK Refactor
Refactor `app/telemetry.py` to remove `asyncpg` dependency.
- **New Behavior**: Fire-and-forget async HTTP requests to `http://gravitas-telemetry:8002`.
- **Fallback**: If the service is down, log to stdout/file, do not crash the application.

## 4. Implementation Plan
1.  **Create Service**: `app/services/telemetry/main.py`.
2.  **Docker**: Add `gravitas-telemetry` to `docker-compose.yml`.
3.  **Refactor Client**: Update `app/telemetry.py` to use `httpx`.
4.  **Migration**: Move `system_telemetry` and `usage_stats` table creation to the new service.

## 5. Alternatives Considered
- **Sidecar Pattern**: Run a fluentd/vector sidecar. Rejected for now to keep the stack simple (Python/Postgres).
- **Message Queue**: Push to Redis/RabbitMQ. Valid, but adds infrastructure complexity (Phase 8+).
