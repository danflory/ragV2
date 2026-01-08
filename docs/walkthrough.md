# Walkthrough: Phase 1 - Database Decomposition

## Goal
Decompose the monolithic `app/database.py` schema initialization logic and distribute ownership of database tables to their respective microservices.

## Changes Implemented

### 1. `app/database.py` (Core Library)
- **Action**: Removed all `CREATE TABLE` statements from the `connect()` method.
- **Result**: This class now only handles connection pooling and provides legacy helper methods for wrappers. It is no longer responsible for schema management.

### 2. `app/services/gatekeeper/database.py` (New)
- **Action**: Created a service-specific database module for Gatekeeper.
- **Ownership**: `audit_log` table.
- **Verification**: Service connects and initializes the schema on startup.

### 3. `app/services/guardian/database.py` (New)
- **Action**: Created a service-specific database module for Guardian.
- **Ownership**: `agent_badges` table.
- **Verification**: Service connects and initializes the schema on startup.

### 4. `app/services/router/database.py` (New)
- **Action**: Created a service-specific database module for Router.
- **Ownership (Provisional)**: `history`, `usage_stats`, `system_telemetry`. (To be moved in RFC-002/Lobby refactor).
- **Verification**: Service connects and initializes the schema on startup.

### 5. Service Entry Points (`main.py`)
- Updated `gatekeeper/main.py`, `guardian/main.py`, and `router/main.py` to call `db.init_schema()` during startup (`lifespan` context manager).
- Updated `Dockerfile.guardian` and `Dockerfile.router` to copy `app/config` needed for database connection settings.
- Updated `requirements/common.txt` to include `asyncpg` for all services.

## Verification Results

### Service Startup Logs

**Gatekeeper:**
```log
INFO:Gravitas_DATABASE:✅ Gatekeeper Schema Initialized (audit_log).
```

**Guardian:**
```log
INFO:Gravitas_DATABASE_GUARDIAN:✅ Guardian Schema Initialized (agent_badges).
```

**Router:**
```log
INFO:Gravitas_DATABASE_ROUTER:✅ Router Schema Initialized.
```

### Database Registry

All tables are present in the `chat_history` database:
```
 Schema |       Name       | Type  |     Owner     
--------+------------------+-------+---------------
 public | agent_badges     | table | Gravitas_user
 public | audit_log        | table | Gravitas_user
 public | history          | table | Gravitas_user
 public | system_telemetry | table | Gravitas_user
 public | usage_stats      | table | Gravitas_user
```

## Conclusion
Phase 1 is complete. The database schema initialization is fully decentralized.
