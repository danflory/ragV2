# Gravitas Access Control Specification (v1.0)

## Overview
This document specifies the access control system for the Gravitas Enterprise architecture. It provides a formal mechanism for governing how **Ghosts** (Agent Identities) interact with **Resources** (Shells, Vaults, Tools, and Configuration).

## 1. Core Concepts

### 1.1 Rational Authorization
Access control in Gravitas is **identity-centric**. Every request must be associated with a `ghost_id`. The Supervisor acts as the "Security Officer," validating that the Ghost has the necessary permissions to perform the requested action.

### 1.2 Access Groups
Permissions are organized into groups to simplify management.

| Group | Description | Default Permissions |
|-------|-------------|----------------------|
| `admin` | Full system control | `*` on all resources |
| `engineer` | System maintenance and debugging | `execute`, `read` on tools/engineer; `read` on logs |
| `librarian` | Knowledge management | `read`, `write` on vaults/*; `execute` on tools/librarian |
| `agent` | Standard execution | `execute` on assigned Shells; `read` on public vaults |
| `guest` | Restricted access | `execute` on L1 models only; no vault access |

## 2. Schema Definition

### 2.1 Permission Format
Permissions are defined as `(action, resource_scope)`.
- **Actions**: `read`, `write`, `execute`, `delete`, `configure`, `grant`.
- **Resource Scopes**:
  - `shells/*` (all models)
  - `shells/l1/*` (local models only)
  - `vaults/internal`
  - `tools/librarian/ingest`
  - `agents/*`

### 2.2 Policy File (`access_policies.yaml`)
Policies are stored in YAML format.

```yaml
version: 1.0
groups:
  admin:
    permissions:
      - action: "*"
        resource: "*"
  
  researcher:
    permissions:
      - action: "execute"
        resource: "shells/*"
      - action: "read"
        resource: "vaults/*"
        
  scout:
    permissions:
      - action: "execute"
        resource: "shells/l1/*"
      - action: "read"
        resource: "vaults/public"

ghost_mappings:
  "Supervisor_Managed_Agent": ["admin"]
  "Librarian": ["librarian"]
  "Scout": ["scout"]
```

## 3. Enforcement Points

### 3.1 Supervisor Router
Every request to `/v1/chat/completions` is intercepted.
- **Check**: `policy_engine.check_permission(ghost_id, "execute", shell_name)`
- **Failure**: Returns `403 Forbidden`.

### 3.2 Tool Execution
Agent tools check for execution permissions.
- **Check**: `policy_engine.check_permission(ghost_id, "execute", tool_name)`

### 3.3 Vault Access
Retrieval and Injection operations check scope.
- **Check**: `policy_engine.check_permission(ghost_id, "read", vault_id)`

## 4. Audit Logging
All authorization decisions (Permit/Deny) are recorded in the `audit_log` table.

| Timestamp | Ghost | Action | Resource | Result | Reason |
|-----------|-------|--------|----------|--------|--------|
| 2026-01-06 12:00:01 | Scout | execute | gemini-1.5-pro | DENIED | Insufficient tier |
| 2026-01-06 12:01:05 | Librarian | write | vaults/core | PERMIT | Group: librarian |

## 5. Implementation Roadmap
1. **Policy Engine**: Load YAML and evaluate logic (`app/services/security/policy_engine.py`).
2. **Audit Logger**: Write to Postgres (`app/services/security/audit_log.py`).
3. **Supervisor Integration**: Update router to call Policy Engine.
4. **Identity**: Integrate JWT to securely pass `ghost_id`.
