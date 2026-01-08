# Current Docker Architecture Analysis

**Question**: Is Docker configured so each component can be tested and updated independently?

**Answer**: **Partially - Yes for infrastructure, NO for application services** ✅ ❌

---

## Current Service Inventory

### Infrastructure Services (✅ Independent)

| Service | Container | Purpose | Independent? | Testable Alone? |
|---------|-----------|---------|--------------|-----------------|
| **PostgreSQL** | `Gravitas_postgres` | Database | ✅ Yes | ✅ Yes |
| **Qdrant** | `Gravitas_qdrant` | Vector DB | ✅ Yes | ✅ Yes |
| **MinIO** | `Gravitas_minio` | Object Storage | ✅ Yes | ✅ Yes |
| **Ollama (GPU 0)** | `Gravitas_ollama` | Generation Models | ✅ Yes | ✅ Yes |
| **Ollama Embed (GPU 1)** | `Gravitas_ollama_embed` | Embedding Models | ✅ Yes | ✅ Yes |

**Status**: ✅ **All infrastructure services are independent**
- Each has its own container
- Each can be started/stopped independently
- Each can be tested in isolation
- Each has dedicated volumes for persistence

---

### Application Services (❌ NOT Independent - Shared Build)

| Service | Container | Purpose | Independent Build? | Issue |
|---------|-----------|---------|-------------------|-------|
| **gravitas_mcp** | `gravitas_mcp` | Development Target | ❌ No | Shares Dockerfile with lobby & supervisor |
| **gravitas_lobby** | `Gravitas_lobby_v2` | Public API | ❌ No | Shares Dockerfile with mcp & supervisor |
| **gravitas_supervisor** | `gravitas_supervisor` | Routing/Security/Guardian | ❌ No | Shares Dockerfile with mcp & lobby |

**Status**: ❌ **Application services are NOT fully independent**

---

## The Problem: Shared Dockerfile

All three application services use the **same Dockerfile**:

```yaml
gravitas_mcp:
  build:
    context: .
    dockerfile: Dockerfile  # ← Same Dockerfile

gravitas_lobby:
  build: .                  # ← Same Dockerfile (implicit)

gravitas_supervisor:
  build: .                  # ← Same Dockerfile (implicit)
```

### What This Means:

1. **Rebuilding one service rebuilds ALL services**
   - If you change lobby code, supervisor gets rebuilt too
   - Wastes time and storage (duplicate images)

2. **Dependency conflicts**
   - All services must have compatible dependencies
   - Example: `google-generativeai` is only needed by Supervisor, but installed in ALL containers

3. **Testing is not isolated**
   - Cannot test supervisor without lobby dependencies being present
   - Integration test failures affect all services

4. **Deployment is coupled**
   - Deploying a supervisor fix requires rebuilding lobby & mcp

---

## Current Independence Assessment

### ✅ What WORKS Independently

```bash
# You CAN do this:
docker-compose up -d Gravitas_postgres    # Start only database
docker-compose up -d Gravitas_qdrant      # Start only vector DB
docker-compose up -d Gravitas_ollama      # Start only Ollama

# Restart infrastructure without touching app
docker-compose restart Gravitas_postgres
```

### ❌ What DOESN'T Work Independently

```bash
# This rebuilds ALL app services (wasteful):
docker-compose up -d --build gravitas_supervisor

# Produces 3 identical images:
# - gravitas-gravitas_mcp
# - gravitas-gravitas_lobby
# - gravitas-gravitas_supervisor
```

---

## Comparison: Current vs. RFC-001 Proposed

| Aspect | Current Architecture | RFC-001 Proposed |
|--------|---------------------|------------------|
| **Service Count** | 3 app services (mcp, lobby, supervisor) | 5 app services (mcp, lobby, gatekeeper, router, guardian) |
| **Dockerfiles** | 1 shared Dockerfile | 5 separate Dockerfiles |
| **Build Independence** | ❌ No - all share same build | ✅ Yes - each has its own build |
| **Dependency Isolation** | ❌ No - all deps in one requirements.txt | ✅ Yes - each service has its own requirements.txt |
| **Test Isolation** | ❌ No - tests run against monolith | ✅ Yes - each service tested independently |
| **Deploy Independence** | ❌ No - changes rebuild all services | ✅ Yes - deploy only changed service |
| **Failure Isolation** | ❌ No - supervisor crash = full outage | ✅ Yes - service failure isolated |

---

## How to Achieve True Independence (RFC-001 Implementation)

### Step 1: Create Separate Dockerfiles

```
.
├── Dockerfile.mcp
├── Dockerfile.lobby
├── Dockerfile.gatekeeper       # NEW
├── Dockerfile.router           # NEW
├── Dockerfile.guardian         # NEW
```

### Step 2: Split Requirements

```
.
├── requirements/
│   ├── common.txt              # Shared dependencies
│   ├── mcp.txt                 # MCP-specific
│   ├── lobby.txt               # Lobby-specific
│   ├── gatekeeper.txt          # Gatekeeper-specific (JWT, policy)
│   ├── router.txt              # Router-specific (provider SDKs)
│   └── guardian.txt            # Guardian-specific (cert management)
```

### Step 3: Update docker-compose.yml

```yaml
gravitas_gatekeeper:
  build:
    context: .
    dockerfile: Dockerfile.gatekeeper  # ← Dedicated Dockerfile
  container_name: gravitas_gatekeeper
  command: uvicorn app.services.gatekeeper.main:app --host 0.0.0.0 --port 8001
  ports:
    - "8001:8001"
  environment:
    - DATABASE_URL=postgresql://...
  networks:
    - Gravitas_net

gravitas_router:
  build:
    context: .
    dockerfile: Dockerfile.router      # ← Dedicated Dockerfile
  container_name: gravitas_router
  command: uvicorn app.services.router.main:app --host 0.0.0.0 --port 8002
  depends_on:
    - gravitas_gatekeeper
    - gravitas_guardian
  environment:
    - GATEKEEPER_URL=http://gravitas_gatekeeper:8001
    - GUARDIAN_URL=http://gravitas_guardian:8003
  ports:
    - "8002:8002"
  networks:
    - Gravitas_net

gravitas_guardian:
  build:
    context: .
    dockerfile: Dockerfile.guardian    # ← Dedicated Dockerfile
  container_name: gravitas_guardian
  command: uvicorn app.services.guardian.main:app --host 0.0.0.0 --port 8003
  ports:
    - "8003:8003"
  environment:
    - DATABASE_URL=postgresql://...
  networks:
    - Gravitas_net
```

---

## Benefits of TRUE Independence

### Development

```bash
# Fix router bug - only rebuild router
docker-compose up -d --build gravitas_router

# Update gatekeeper policy - only restart gatekeeper
docker-compose restart gravitas_gatekeeper

# Test guardian in isolation
docker-compose up -d gravitas_guardian Gravitas_postgres
pytest tests/unit/test_guardian.py
```

### Deployment

```bash
# Deploy only router changes to production
docker build -f Dockerfile.router -t gravitas_router:v2.1 .
docker push gravitas_router:v2.1

# Zero downtime: update only router, gatekeeper & guardian still running
kubectl set image deployment/router router=gravitas_router:v2.1
```

### Debugging

```bash
# Gatekeeper failing? Check its logs in isolation
docker logs gravitas_gatekeeper --tail 100

# Guardian slow? Profile just guardian
docker stats gravitas_guardian

# Router crashing? Others still healthy
curl http://localhost:8001/health  # ✅ Gatekeeper still responds
curl http://localhost:8003/health  # ✅ Guardian still responds
curl http://localhost:8002/health  # ❌ Router down (isolated failure)
```

---

## Summary

### Current State (As-Is)

| Component Type | Independent? | Reason |
|----------------|--------------|--------|
| **Infrastructure** | ✅ YES | Each has own container, volume, config |
| **Application Services** | ❌ NO | All share same Dockerfile and dependencies |

### Recommendation

**To achieve true component independence**, you need to implement **RFC-001: Supervisor Decomposition**, which includes:

1. ✅ Separate Dockerfiles for each service
2. ✅ Split `requirements.txt` into service-specific deps
3. ✅ Independent CI/CD pipelines per service
4. ✅ Service-specific integration tests
5. ✅ Isolated failure domains

**Without RFC-001**, you have **partial independence** (infrastructure yes, apps no).

**With RFC-001**, you achieve **full independence** (infrastructure + apps).

---

## Next Steps

1. **Review RFC-001** to understand the full architectural proposal
2. **Decide**: Implement RFC-001 or keep current shared-build architecture
3. **If proceeding**: Start with Phase 1 (Guardian extraction) as lowest-risk change

---

**Document Created**: 2026-01-07  
**Related**: [RFC-001](file:///home/dflory/dev_env/Gravitas/docs/RFC-001-SupervisorDecomposition.md)
