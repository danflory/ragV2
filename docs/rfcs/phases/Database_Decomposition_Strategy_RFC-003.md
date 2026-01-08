# RFC-003: Database Decomposition Strategy

| Metadata | Value |
| :--- | :--- |
| **RFC ID** | RFC-003 |
| **Status** | ✅ COMPLETE |
| **Created** | 2026-01-08 |
| **Completed** | 2026-01-07 |
| **Author** | Antigravity |
| **Topic** | Microservices Architecture |

## 1. Summary
Dismantle the monolithic `app/database.py` initialization logic. Transition to a model where each microservice owns its own data schema and database interactions.

## 2. Motivation
The current `app/database.py` acts as a "God Object," initializing tables for History, Telemetry, Audits, and Badges whenever *any* service connects.
- **Risk**: A bug in the history table schema definition could crash the Gatekeeper service on startup, even though Gatekeeper doesn't use history.
- **Coupling**: It reinforces the pattern that every service has access to every table, violating the principle of least privilege.

## 3. Proposed Design

### 3.1 Schema Ownership
Assign "Data Sovereignty" to specific services:
- **Gatekeeper Service**: Owns `audit_log` table.
- **Guardian Service**: Owns `agent_badges` table.
- **Telemetry Service** (RFC-002): Owns `system_telemetry` and `usage_stats`.
- **Lobby Service** (Future): Owns `history` (chat logs).

### 3.2 Implementation Strategy
1.  **Remove Auto-Init**: Delete the massive `CREATE TABLE IF NOT EXISTS` block in `app/database.py`.
2.  **Service-Specific Init**: Move table creation logic to the `startup` event of each respective microservice (e.g., `app/services/gatekeeper/main.py` -> `on_startup`).
3.  **Scoped Connections**: (Optional for Phase 7.5, Required for Phase 8) Create separate Postgres users for each service (e.g., `gravitas_gatekeeper` user) with permissions only on their owned tables.

## 4. Migration Plan
1.  **Step 1**: Duplicate the table creation SQL into `app/services/<service>/database.py` for each service.
2.  **Step 2**: Verify each service can start and manage its own tables.
3.  **Step 3**: Strip the central `app/database.py` down to a simple connection pool factory without schema logic.

## 5. Alternatives Considered
- **Alembic Migrations**: Standardize on Alebmic for all migrations.
    - *Pros*: Robust version control.
    - *Cons*: Adds complexity to the current "Reflexive Schema" (code-first) philosophy the user seems to prefer. We will stick to code-first for now but decentralized.
