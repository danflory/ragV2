# RFC-003: Database Decomposition

**Status**: COMPLETE ✅  
**Created**: 2026-01-07  
**Author**: Antigravity  
**Triggered By**: Phase 1 Core Architecture Cleanup

---

## 1. Abstract

This RFC formalizes the dismantling of the monolithic `app/database.py` initialization logic in favor of a decentralized, service-specific schema ownership model. This change ensures that each microservice (Gatekeeper, Guardian, Router, etc.) maintains its own data structures, reducing cross-service coupling and preparing the system for independent scaling.

---

## 2. Motivation

### The Problem
In the initial monolithic design, `app/database.py` contained hardcoded `CREATE TABLE` statements for the entire system.
1. **Tight Coupling**: Any service update requiring a schema change forced a rebuild of the core database library.
2. **Security Risk**: All services had access to the entire schema, violating the principle of least privilege.
3. **Inflexibility**: Different services could not iterate on their data models independently.

### Goals
1. **Service Autonomy**: Each service owns its tables and initialization logic.
2. **Library Simplification**: `app/database.py` becomes a thin wrapper for connection pooling.
3. **Structural Clarity**: Data models are colocated with the services that use them.

---

## 3. Component Breakdown

### 3.1 Core Library (`app/database.py`)
- **Action**: Removed all `init_schema()` SQL strings.
- **Responsibility**: Provides `asyncpg` connection pooling and basic connectivity checks.

### 3.2 Service Schema Ownership
| Service | Component | Tables Owned |
| :--- | :--- | :--- |
| **Gatekeeper** | `app/services/gatekeeper/database.py` | `audit_log` |
| **Guardian** | `app/services/guardian/database.py` | `agent_badges` |
| **Router** | `app/services/router/database.py` | `history`, `system_telemetry`*, `usage_stats`* |

> [!NOTE]
> Telemetry and usage stats are provisionally owned by the Router until Phase 3 (Telemetry Decoupling).

---

## 4. Verification & Testing

To verify the successful decomposition, perform the following steps:

### 4.1 Service Startup Validation
Run each service and monitor the logs for successful connection and schema initialization.

**Commands**:
```bash
# Start services individually for log inspection
python -m app.services.gatekeeper.main
python -m app.services.guardian.main
python -m app.services.router.main
```

**Expected Log Output**:
```text
INFO:Gravitas_DATABASE:✅ Gatekeeper Schema Initialized (audit_log).
INFO:Gravitas_DATABASE_GUARDIAN:✅ Guardian Schema Initialized (agent_badges).
INFO:Gravitas_DATABASE_ROUTER:✅ Router Schema Initialized.
```

### 4.2 Database Integrity Check
Verify that all required tables are present in the PostgreSQL instance.

**Command**:
```bash
PGPASSWORD=Gravitas_pass psql -h localhost -U Gravitas_user -d chat_history -c "\dt"
```

**Expected Results**:
- `audit_log`
- `agent_badges`
- `history`
- `system_telemetry`
- `usage_stats`

### 4.3 Connectivity Test
Verify that services can perform basic CRUD operations on their own tables.
*   **Gatekeeper**: Successfully log a request to `audit_log`.
*   **Guardian**: Successfully certifiy an agent via `agent_badges`.

---

## 5. Success Criteria

- [x] No `CREATE TABLE` statements remain in `app/database.py`.
- [x] All services successfully initialize their own schemas on startup.
- [x] Schema changes in one service do not affect the build of others.
- [x] Database credentials are restricted to the relevant service schemas (Phase 7+ Hardening).

---

## 6. Revision History
- **2026-01-07**: Initial consolidation from Phase 1 walkthrough documents.
- **2026-01-07**: Added explicit verification steps and expected results.
