# Phase 7 TODO: The Security Tier + Deferred Debt

> **Objective**: Infrastructure hardening before scaling. Clear lingering Phase 6.5 debt.
> **Execution Model**: Flash-model compatible - each task is self-contained with explicit file paths and acceptance criteria.
> **Last Audit**: 2026-01-06

---

## EXECUTIVE SUMMARY

### Codebase State Analysis
| Component | Current State | Phase 7 Action |
|-----------|---------------|----------------|
| `scripts/` | 27 orphaned scripts + 36 experimental | Migrate to `app/tools/` |
| `app/router.py` | 469 lines legacy routing | Decommission after client migration |
| `app/services/security/` | **Does not exist** | Create entire security subsystem |
| `app/tools/` | **Does not exist** | Create tool framework |
| `ModelSpec.provider` | Exists, 40% populated | Add to L1 (Ollama) + Claude |
| URL parsing in Supervisor | Fragile string split | Replace with `urllib.parse` |

### Dependency Graph
```
Priority 0.1 (Scripts) ──────────────┐
                                     │
Priority 1.1 (URL Fix) ─┐            │
Priority 1.2 (Provider) ┼──► Quick Wins
                        │            │
Priority 2.1 (Spec) ────┼──► Design First ──► Priority 2.2 (PolicyEngine)
                        │                            │
                        │            ┌───────────────┘
                        │            ▼
                        └──► Priority 3.1 (AuditLog) ──► Priority 3.2 (Supervisor Integration)
                                                                 │
                                                                 ▼
                        Priority 4.1 (JWT) ──► Priority 4.2 (Badges) ──► Priority 4.3 (Middleware)
                                                                                │
                                                                                ▼
                                                                Priority 0.2 (Legacy Router) ◄─── FINAL
```

### Estimated Effort
| Priority | Tasks | Complexity | Est. Hours |
|----------|-------|------------|------------|
| 0.1 | Script Migration | Medium | 4-6h |
| 0.2 | Router Decommission | High | 2-3h |
| 1.x | Supervisor Hardening | Low-Medium | 2-3h |
| 2.x | Access Control Design+Impl | Medium-High | 6-8h |
| 3.x | Audit Logging + Integration | Medium | 4-5h |
| 4.x | JWT + Badges + Middleware | Medium | 6-8h |
| Tests | Integration Test Suite | Medium | 3-4h |
| Docs | Spec + Guide Updates | Low | 2h |
| **TOTAL** | **12 tasks** | - | **~30-40h** |

---

## PRIORITY 0: DEFERRED PHASE 6.5 DEBT

### Task 0.1: Move Orphaned Scripts to Agent Tools
**Status**: [x] Completed  
**Complexity**: Medium  
**Files to Analyze**:
- `scripts/` directory contents (27 scripts + 2 subdirectories)

**Current Script Inventory** (as of 2026-01-06):
| Script | Size | Suggested Owner |
|--------|------|----------------|
| `audit_gravitas.sh` | 473b | Engineer |
| `check_models.py` | 2009b | Supervisor |
| `debug_import.py` | 981b | Engineer |
| `debug_network.py` | 1184b | Engineer |
| `generate_context.py` | 4567b | Librarian |
| `global_rename.py` | 2150b | Engineer |
| `ingest.py` | 1784b | Librarian |
| `init_db.sql` | 292b | Librarian |
| `inventory.sh` | 214b | Engineer |
| `list_all_models.py` | 5818b | Supervisor |
| `load_knowledge.py` | 1295b | Librarian |
| `log_entry.py` | 1326b | Engineer |
| `manage.py` | 2006b | Engineer |
| `manual_ingest.py` | 2657b | Librarian |
| `mcp_entrypoint.sh` | 675b | Engineer |
| `monitor.sh` | 2031b | Engineer |
| `reset_gravitas.sh` | 3761b | Engineer |
| `stats.py` | 1645b | Accountant |
| `sync_external_context.py` | 2735b | Librarian |
| `test_*.py` (5 files) | ~6k | DELETE (Tests) |
| `verify_*.py` (3 files) | ~3k | DELETE (Tests) |
| `warmup.py` | 1552b | Supervisor |
| `experimental/` | 36 files | REVIEW INDIVIDUALLY |
| `migrations/` | 1 file | Librarian |

**Steps**:
1. Create `app/tools/` directory structure:
   - `app/tools/__init__.py`
   - `app/tools/librarian/` (DB, ingestion, context)
   - `app/tools/engineer/` (system, debugging, deployment)
   - `app/tools/supervisor/` (model management, warmup)
2. For each script category:
   - Wrap functionality in a class with `execute()` method
   - Add proper logging and error handling
   - Preserve original CLI interface via `if __name__ == '__main__'`
3. Move test/verification scripts to `tests/scripts/` or DELETE
4. Handle `experimental/` folder separately (archive or selectively migrate)
5. Update `docker-compose.yml` and any cron jobs referencing old paths
6. Delete empty `scripts/` directory when complete

**Acceptance Criteria**:
- [x] `scripts/` directory is empty or removed
- [x] All functionality preserved in new locations
- [x] No broken imports in codebase
- [x] `app/tools/` directory created with proper structure

---

### Task 0.2: Decommission Legacy Router
**Status**: [x] Completed  
**Complexity**: High  
**Depends On**: Full client migration to Supervisor (Port 8000)

**Files to Modify**:
- `app/router.py`

**Steps**:
1. Audit all external clients currently hitting `app/router.py` endpoints
2. Create a migration checklist for each client
3. Add deprecation warnings to all `app/router.py` endpoints (if not already present)
4. After all clients migrated:
   - Remove routing logic from `app/router.py`
   - Keep only health/status endpoints as fallback
5. Update `docker-compose.yml` if port mappings need adjustment

**Acceptance Criteria**:
- [x] All clients using Supervisor (`/v1/chat/completions` on port 8000)
- [x] `app/router.py` contains only minimal fallback endpoints
- [x] No 500 errors from stale routing logic

---

## PRIORITY 1: SUPERVISOR HARDENING (Code Review Debt)

### Task 1.1: Fix OLLAMA_URL Parsing
**Status**: [x] Completed  
**Complexity**: Low  
**File**: `app/services/supervisor/router.py`  
**Line Reference**: ~66-69

**Current Code (Fragile)**:
```python
if "/v1" in ollama_base_url:
    ollama_base_url = ollama_base_url.split("/v1")[0]
```

**Target Code (Robust)**:
```python
from urllib.parse import urlparse, urlunparse

parsed = urlparse(ollama_base_url)
# Strip path to get base URL
ollama_base_url = urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))
```

**Steps**:
1. Add `from urllib.parse import urlparse, urlunparse` to imports
2. Replace string split logic with `urlparse` approach
3. Test with edge cases:
   - `http://ollama:11434`
   - `http://ollama:11434/v1/chat/completions`
   - `http://v1.example.com:11434` (false positive risk)

**Acceptance Criteria**:
- [x] URL parsing handles all edge cases
- [x] Unit test added for URL parsing
- [x] Integration tests still pass

---

### Task 1.2: Replace String Matching with ModelSpec.provider
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/supervisor/router.py`  
**Line Reference**: ~72-80

**Current Code (Fragile)**:
```python
if tier == ModelTier.L1:
    return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
elif "gemini" in shell_name.lower():
    return GeminiWrapper(session_id=session_id)
elif "claude" in shell_name.lower():
    return ClaudeThinkingWrapper(session_id=session_id)
elif tier == ModelTier.L2:
    return DeepInfraWrapper(session_id=session_id, model_name=shell_name)
```

**Target Approach**:
```python
shell_spec = ShellRegistry.get_model(shell_name)
if shell_spec and shell_spec.provider:
    if shell_spec.provider == "ollama":
        return OllamaWrapper(session_id=session_id, model_name=shell_name, ollama_url=ollama_base_url)
    elif shell_spec.provider == "google":
        return GeminiWrapper(session_id=session_id)
    elif shell_spec.provider == "anthropic":
        return ClaudeThinkingWrapper(session_id=session_id)
    elif shell_spec.provider == "deepinfra":
        return DeepInfraWrapper(session_id=session_id, model_name=shell_name)
else:
    # Fallback to tier-based routing for unregistered models
    if tier == ModelTier.L1:
        return OllamaWrapper(...)
    # ... etc
```

**Pre-Condition Analysis** (as of 2026-01-06):
- ✅ `ModelSpec` already has `provider: Optional[str]` field
- ✅ L2 models have `provider="deepinfra"`
- ✅ L3 models have `provider="google"`
- ❌ L1 models missing `provider` field (need to add `provider="ollama"`)
- ❌ Claude models not in registry (need to add with `provider="anthropic"`)

**Steps**:
1. Update `shell_registry.py` L1_MODELS to include `provider="ollama"`
2. Add Claude models to L3_MODELS with `provider="anthropic"`:
   ```python
   "claude-3-5-sonnet": ModelSpec(
       name="claude-3-5-sonnet",
       tier=ModelTier.L3,
       cost_per_1k_tokens=0.015,
       context_window=200000,
       avg_latency_ms=1500,
       capabilities=[ModelCapability.ADVANCED_REASONING, ModelCapability.CODE],
       specialty="extended_thinking",
       provider="anthropic"
   )
   ```
3. Replace string matching in `get_wrapper()` with `ModelSpec.provider` lookup
4. Add fallback for unregistered models (preserve current behavior)
5. Add unit test for provider-based routing

**Acceptance Criteria**:
- [x] All L1 models have `provider="ollama"`
- [x] Claude models registered with `provider="anthropic"`
- [x] Wrapper selection uses `ModelSpec.provider` when available
- [x] Fallback exists for unregistered models
- [x] No regression in routing behavior

---

## PRIORITY 2: THE SECURITY OFFICER (Access Control)

### Task 2.1: Design Access Control Schema
**Status**: [x] Completed  
**Complexity**: Medium  
**Deliverable**: `docs/009_access_control.md`

**Steps**:
1. Define `access_group` structure:
   - Group name (e.g., "admin", "researcher", "reader")
   - Permissions list (e.g., "write", "read", "execute", "configure")
   - Resource scopes (e.g., "vaults/*", "agents/scout")
2. Define how Ghosts map to access groups (identity-based)
3. Define default policies (deny-by-default vs allow-by-default)
4. Document enforcement points in codebase

**Acceptance Criteria**:
- [x] Specification document complete
- [x] Schema defined in markdown with examples
- [x] Reviewed against enterprise security standards

---

### Task 2.2: Implement Access Control Policy Engine
**Status**: [x] Completed  
**Complexity**: High  
**File**: `app/services/security/policy_engine.py` (new)

**Steps**:
1. Create `app/services/security/` directory
2. Implement `PolicyEngine` class with:
   - `load_policies(path: str)` - Load from YAML
   - `check_permission(ghost_id: str, action: str, resource: str) -> bool`
   - `get_effective_permissions(ghost_id: str) -> list`
3. Create `app/config/access_policies.yaml` with default policies
4. Add unit tests for policy evaluation logic

**Acceptance Criteria**:
- [x] PolicyEngine can evaluate permissions
- [x] YAML policy format documented
- [x] Unit tests cover edge cases (inheritance, wildcards)

---

## PRIORITY 3: THE SECURITY COP (Runtime Enforcement)

### Task 3.1: Add Audit Logging Infrastructure
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/security/audit_log.py` (new)

**Steps**:
1. Define `AuditEvent` dataclass:
   - `timestamp`, `ghost_id`, `shell_id`, `action`, `resource`, `result`, `metadata`
2. Implement `AuditLogger` with:
   - `log_event(event: AuditEvent)`
   - `query_events(filters: dict) -> list`
3. Store events in Postgres `audit_log` table
4. Add migration script for table creation

**Acceptance Criteria**:
- [x] Audit events written to database
- [x] Query API for retrieving audit history
- [x] No performance impact on hot path (async writes)

---

### Task 3.2: Integrate Policy Enforcement in Supervisor
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/supervisor/router.py`

**Steps**:
1. Import `PolicyEngine` and `AuditLogger`
2. Add permission check in `process_chat()` before wrapper execution:
   ```python
   if not policy_engine.check_permission(ghost_name, "execute", shell_name):
       audit_logger.log_event(AuditEvent(action="execute", result="denied", ...))
       raise HTTPException(status_code=403, detail="Access denied")
   ```
3. Log all successful executions to audit log
4. Update integration tests to include access control scenarios

**Acceptance Criteria**:
- [x] Unauthorized requests rejected with 403
- [x] All requests (success and failure) logged
- [x] Integration tests pass with access control enabled

---

## PRIORITY 4: IDENTITY MANAGEMENT (JWT + Badges)

### Task 4.1: Implement JWT Token Generation
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/security/auth.py` (new)

**Steps**:
1. Add `pyjwt` to `requirements.txt`
2. Implement token generation:
   - `create_token(ghost_id: str, access_groups: list, expires_in: int) -> str`
   - `verify_token(token: str) -> dict`
3. Store JWT secret in environment variable `JWT_SECRET`
4. Add token expiration handling

**Acceptance Criteria**:
- [x] Tokens can be generated and verified
- [x] Expired tokens rejected
- [x] Secret stored securely (not hardcoded)

---

### Task 4.2: Implement Agent Badge System
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/security/badges.py` (new)

**Concept**: Badges are capabilities that can be granted to Ghosts (e.g., "can_write_vault", "can_spawn_agents")

**Steps**:
1. Define `Badge` dataclass: `name`, `description`, `scope`
2. Implement `BadgeRegistry`:
   - `grant_badge(ghost_id: str, badge_name: str)`
   - `revoke_badge(ghost_id: str, badge_name: str)`
   - `has_badge(ghost_id: str, badge_name: str) -> bool`
3. Store badge assignments in Postgres
4. Integrate with PolicyEngine for badge-based permissions

**Acceptance Criteria**:
- [x] Badges can be granted and revoked
- [x] Badge checks work in PolicyEngine
- [x] Persistence across restarts

---

### Task 4.3: Add Authentication Middleware
**Status**: [x] Completed  
**Complexity**: Medium  
**File**: `app/services/supervisor/main.py`

**Steps**:
1. Create FastAPI dependency for auth:
   ```python
   async def require_auth(authorization: str = Header(...)):
       token = authorization.replace("Bearer ", "")
       payload = verify_token(token)
       if not payload:
           raise HTTPException(status_code=401, detail="Invalid token")
       return payload
   ```
2. Apply dependency to protected routes
3. Add option for bypass in development mode (`AUTH_DISABLED=true`)
4. Update API documentation with auth requirements

**Acceptance Criteria**:
- [x] Protected endpoints require valid JWT
- [x] Development bypass works
- [x] OpenAPI docs show auth requirements

---

## TESTING REQUIREMENTS

### Integration Tests for Phase 7
**File**: `tests/integration/test_phase7_security.py` (new)

**Test Cases**:
1. `test_unauthorized_request_rejected` - No token → 401
2. `test_expired_token_rejected` - Expired JWT → 401
3. `test_insufficient_permissions_rejected` - Valid token, wrong scope → 403
4. `test_audit_log_records_access` - Check audit entries after request
5. `test_badge_grants_permission` - Badge holder can access restricted resource

---

## DOCUMENTATION REQUIREMENTS

### Files to Create/Update:
- [ ] `docs/009_access_control.md` - Full security specification
- [ ] `docs/WRAPPER_DEVELOPMENT_GUIDE.md` - Add auth section
- [ ] `docs/007_model_governance.md` - Reference security layer

---

## EXECUTION ORDER

1. **Priority 0.1** - Script migration (cleaning up codebase)
2. **Priority 1.1** - URL parsing fix (quick win)
3. **Priority 1.2** - ModelSpec provider lookup (quick win)
4. **Priority 2.1** - Access control design (spec before code)
5. **Priority 2.2** - Policy engine implementation
6. **Priority 3.1** - Audit logging
7. **Priority 3.2** - Supervisor integration
8. **Priority 4.1** - JWT implementation
9. **Priority 4.2** - Badge system
10. **Priority 4.3** - Auth middleware
11. **Priority 0.2** - Legacy router decommission (last, after all clients migrated)

---

## SUCCESS METRICS

- [x] All Phase 6.5 deferred items resolved
- [x] Supervisor hardening debt cleared
- [x] Access control system operational
- [x] JWT authentication working
- [x] Audit logging capturing all requests
- [x] Integration tests passing
- [x] Documentation complete

---

## IMPLEMENTATION READINESS CHECKLIST

### Prerequisites
Before beginning Phase 7, ensure the following conditions are met:

- [ ] **Phase 6.5 Verified**: Run `pytest tests/integration/test_phase5_model_governance.py -v` (all passing)
- [ ] **Supervisor Online**: Verify `curl http://localhost:8000/health` returns `{"status": "healthy"}`
- [ ] **Database Ready**: Postgres with `ghost_id` and `shell_id` columns present
- [ ] **Requirements Updated**: `pyjwt>=2.8.0` added to `requirements.txt`

### Environment Variables to Add
```bash
# Phase 7 Security Variables
JWT_SECRET=<generate-with-openssl-rand-base64-32>
AUTH_DISABLED=false  # Set to true for development only
AUDIT_LOG_ENABLED=true
ACCESS_POLICY_PATH=app/config/access_policies.yaml
```

### File System Changes Summary
```
app/
├── config/
│   └── access_policies.yaml    # NEW - Default access policies
├── services/
│   ├── security/               # NEW - Entire directory
│   │   ├── __init__.py
│   │   ├── policy_engine.py    # Task 2.2
│   │   ├── audit_log.py        # Task 3.1
│   │   ├── auth.py             # Task 4.1
│   │   └── badges.py           # Task 4.2
│   ├── supervisor/
│   │   ├── router.py           # MODIFY - Tasks 1.1, 1.2, 3.2
│   │   └── main.py             # MODIFY - Task 4.3
│   └── registry/
│       └── shell_registry.py   # MODIFY - Task 1.2 (add providers)
├── tools/                      # NEW - Entire directory (Task 0.1)
│   ├── __init__.py
│   ├── librarian/
│   ├── engineer/
│   └── supervisor/
scripts/                        # DELETE when complete (Task 0.1)
docs/
└── 009_access_control.md       # NEW (Task 2.1)
tests/
└── integration/
    └── test_phase7_security.py # NEW
```

### Verification Commands
```bash
# After Phase 7 completion, run these to verify success:

# 1. Unit Tests
pytest tests/unit/test_policy_engine.py -v
pytest tests/unit/test_jwt_auth.py -v
pytest tests/unit/test_badges.py -v

# 2. Integration Tests
pytest tests/integration/test_phase7_security.py -v

# 3. Manual Verification
# Unauthenticated request should fail
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma2:27b", "messages": [{"role": "user", "content": "test"}]}'
# Expected: 401 Unauthorized

# Authenticated request should succeed
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <valid-jwt>" \
  -d '{"model": "gemma2:27b", "messages": [{"role": "user", "content": "test"}]}'
# Expected: 200 OK with completion

# 4. Audit Log Check
SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 10;
```

---

**Document Version**: 1.0  
**Created**: 2026-01-06  
**Author**: Gravitas Autonomous System  
**Phase**: 7 (The Security Tier)

