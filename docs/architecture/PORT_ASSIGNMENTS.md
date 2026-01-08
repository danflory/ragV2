# Gravitas Port Assignment Reference

**Last Updated**: 2026-01-08

## Port Mapping Explained

Docker port mappings follow the format: `HOST:CONTAINER` (also called `EXTERNAL:INTERNAL`)

- **External Port** (Host): Port accessible from your host machine (`localhost:<PORT>`)
- **Internal Port** (Container): Port the service listens on inside the Docker network

Services communicate with each other using **internal ports** and **container names** as hostnames.

---

## Current Port Assignments

### Infrastructure Services

| Service | Container Name | External → Internal | Protocol | Description |
|---------|---------------|---------------------|----------|-------------|
| **PostgreSQL** | `Gravitas_postgres` | `5432:5432` | TCP | Database - Chat History & Audit Logs |
| **Qdrant** | `Gravitas_qdrant` | `6333:6333` | HTTP | Vector Database - Main API |
| **Qdrant** | `Gravitas_qdrant` | `6334:6334` | gRPC | Vector Database - gRPC Interface |
| **MinIO** | `Gravitas_minio` | `9000:9000` | HTTP/S3 | Object Storage - S3 API |
| **MinIO** | `Gravitas_minio` | `9001:9001` | HTTP | Object Storage - Web Console |
| **Ollama (GPU 0)** | `Gravitas_ollama` | `11434:11434` | HTTP | L1 Model Server (Titan RTX) |
| **Ollama Embed (GPU 1)** | `Gravitas_ollama_embed` | `11435:11434` | HTTP | Embedding Model Server (GTX 1060) |

### Application Services (Microservices)

| Service | Container Name | External → Internal | Protocol | Description |
|---------|---------------|---------------------|----------|-------------|
| **MCP Core** | `gravitas_mcp` | `8001:8000` | HTTP | Main MCP Interface (Development) |
| **Lobby (API)** | `Gravitas_lobby_v2` | `5050:5050` | HTTP | Public Entry Point / Main API |
| **Gatekeeper** | `gravitas_gatekeeper` | `8002:8001` | HTTP | Security: Auth, Policy, Audit |
| **Guardian** | `gravitas_guardian` | `8003:8003` | HTTP | Identity: Certificates & Badges |
| **Router** | `gravitas_router` | `8005:8004` | HTTP | Traffic Routing: L1/L2/L3 |

---

## Internal-Only Communication

Services communicate internally using container names as DNS hostnames. Examples:

```bash
# Router calls Gatekeeper for auth
http://gravitas_gatekeeper:8001/validate

# Router calls Guardian for badges
http://gravitas_guardian:8003/v1/badge/verify

# Services query Ollama models
http://Gravitas_ollama:11434/v1/chat/completions

# Embeddings via dedicated GPU
http://Gravitas_ollama_embed:11434/api/embeddings
```

> [!NOTE]
> Internal communication uses **internal ports** (right side of the mapping). External port mappings are only for host machine access.

---

## Reserved / Planned Ports

### Upcoming Services (RFC Implementation)

| Service | External | Internal | Status | RFC Reference |
|---------|----------|----------|--------|---------------|
| **Telemetry** | `8007` | `8006` | PLANNED | RFC-002 |
| **Neo4j Graph DB** | `7474`, `7687` | `7474`, `7687` | PLANNED | Phase 9 (Graph RAG) |

---

## Port Allocation Strategy

### Current Port Ranges

- **5000-5999**: Public-facing APIs (Lobby)
- **6000-6999**: Storage infrastructure (Qdrant)
- **7000-7999**: Reserved for Graph DB (Neo4j)
- **8000-8099**: Microservices (Internal APIs)
- **9000-9999**: Object storage (MinIO)
- **11400-11499**: Model servers (Ollama instances)

### Next Available Ports

- **Microservices**: `8007` (external), `8006` (internal) ← **Next telemetry service**
- **Infrastructure**: `7474`, `7687` (Neo4j when added)

---

## Access Examples

### From Host Machine

```bash
# Query main API
curl http://localhost:5050/health

# Check Gatekeeper
curl http://localhost:8002/health

# Check Guardian
curl http://localhost:8003/health

# Check Router
curl http://localhost:8005/health

# Access MinIO console
open http://localhost:9001

# Access Qdrant dashboard
open http://localhost:6333/dashboard
```

### From Inside Docker Network

```bash
# Services use internal ports and container names
docker exec -it gravitas_router curl http://gravitas_gatekeeper:8001/health
docker exec -it gravitas_gatekeeper curl http://Gravitas_postgres:5432
```

---

## Port Conflict Prevention

> [!IMPORTANT]
> Before adding a new service, check this document and update it to prevent port conflicts.

### Pre-deployment Checklist

1. Choose external port from available range
2. Choose internal port (can match external or use service's default)
3. Update this document
4. Update `docker-compose.yml`
5. Commit both changes together

---

## Why Different Internal/External Ports?

Some services use different mappings to:

1. **Avoid conflicts**: Multiple Ollama instances (GPU 0 on 11434, GPU 1 on 11435 externally, both use 11434 internally)
2. **Security**: Expose non-standard ports externally to reduce scanning attacks
3. **Flexibility**: Allow future port reorganization without changing service code

**Best Practice**: Internal ports should match the service's default when possible (e.g., PostgreSQL always uses 5432 internally).
