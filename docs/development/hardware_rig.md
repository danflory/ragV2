# Gravitas Hardware Configuration
**Last Updated**: 2026-01-07  
**Status**: ACTIVE

---

## 1. System Overview

**Host OS**: Windows 10 Pro  
**Development Environment**: WSL2 (Ubuntu)  
**Platform**: Gravitas - Local-first AI development platform with 3-tier inference architecture

---

## 2. Compute Hardware

### CPU & Memory
- **Processor**: AMD Ryzen 5 1600
  - 6 Cores / 12 Threads
  - Base Clock: 3.2 GHz
- **System RAM**: 16GB DDR4

### GPU Configuration (Dual-GPU Architecture)

#### GPU 0: NVIDIA Titan RTX (Primary Compute)
- **VRAM**: 24GB GDDR6
- **Role**: L1 Local LLM Inference / Training
- **Services**: `Gravitas_ollama` (Port 11434)
- **Current Model**: `deepseek-coder-v2:16b` (~16GB VRAM)
- **VRAM Management**: 
  - Hard limit: 24GB
  - Safety buffer: 2GB minimum free
  - Overload protection: Auto-promote to L2 when VRAM < 2GB

#### GPU 1: NVIDIA GTX 1060 (Embedding Engine)
- **VRAM**: 6GB GDDR5
- **Role**: Dedicated embedding workloads
- **Services**: `Gravitas_ollama_embed` (Port 11435)
- **Models**: 
  - `nomic-embed-text:latest`
  - `BAAI/bge-m3`
  - `BAAI/bge-reranker-v2-m3`

**Benefits**:
- ✅ Parallel processing (embeddings don't block generation)
- ✅ GPU 1 runs productive workloads (not idle display duty)
- ✅ Frees 6-7GB on Titan RTX for larger contexts

---

## 3. Storage Configuration

### C: Drive - Primary Storage (M.2 NVMe SSD)
- **Capacity**: 931GB (1TB)
- **Used**: 334GB (36%)
- **Available**: 598GB
- **Type**: M.2 NVMe SSD (Fast)
- **Contains**:
  - Windows OS
  - WSL2 virtual disk (`ext4.vhdx`)
  - **Gravitas** (see paths below)
  - **Docker data** (via WSL2)

### D: Drive - Secondary Storage
- **Capacity**: 232GB
- **Used**: 4GB (2%)
- **Available**: 228GB
- **Type**: [SSD/HDD - TBD]
- **Use**: Available for expansion

### F: Drive - Backup Storage
- **Capacity**: 10TB
- **Used**: 736GB (8%)
- **Available**: 9.3TB
- **Type**: [Likely HDD based on size]
- **Use**: BorgBackup repository (`/mnt/f/dockerDesktopFromBorgeBackup/`)

---

## 4. Gravitas Installation Paths

### WSL2 Path (Linux):
```bash
/home/dflory/dev_env/Gravitas
```

### Windows Path (from Windows Explorer):
```
\\wsl.localhost\Ubuntu\home\dflory\dev_env\Gravitas
```
Or alternatively:
```
\\wsl$\Ubuntu\home\dflory\dev_env\Gravitas
```

### Physical Location:
**C: Drive** (inside WSL2 virtual disk)
```
C:\Users\msdn\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu...\LocalState\ext4.vhdx
  └─ (Virtual ext4 filesystem containing:)
      └─ /home/dflory/dev_env/Gravitas/
```

**Current Size**: ~41GB
- Code: ~100MB
- Models: ~26GB (`data/ollama_models/` + `data/ollama_embed_models/`)
- Databases: ~500MB (`data/postgres_data/`, `data/qdrant/`)
- Other: ~14.4GB

---

## 5. Docker Configuration

### Docker Desktop Location:
**Docker is running via WSL2 backend**, not Windows Docker Desktop.

### Docker Data Paths:

#### Container Data (Volume Mounts):
All Docker containers mount volumes from the Gravitas `data/` folder:

| Container | Internal Path | Host Mount (WSL) | Size |
|-----------|---------------|------------------|------|
| `Gravitas_ollama` | `/root/.ollama` | `/home/dflory/dev_env/Gravitas/data/ollama_models` | 22GB |
| `Gravitas_ollama_embed` | `/root/.ollama` | `/home/dflory/dev_env/Gravitas/data/ollama_embed_models` | 3.9GB |
| `Gravitas_postgres` | `/var/lib/postgresql/data` | `/home/dflory/dev_env/Gravitas/data/postgres_data` | 203MB |
| `Gravitas_qdrant` | `/qdrant/storage` | `/home/dflory/dev_env/Gravitas/data/qdrant` | 203MB |
| `Gravitas_minio` | `/data` | `/home/dflory/dev_env/Gravitas/data/minio` | 4.4MB |

**All Docker data persists in**: `/home/dflory/dev_env/Gravitas/data/`  
**Physical location**: C: Drive (inside WSL2 ext4.vhdx)

#### Docker System Files:
- **WSL2 Docker VM**: Runs as `docker-desktop` WSL distribution
- **Docker images/layers**: Stored in WSL2 filesystem on C:
- **Total Docker footprint**: ~26GB (models) + overhead

---

## 6. The 3L Architecture (Inference Economy)

Gravitas uses a **3-tier cascade** to minimize cost while maximizing quality:

### L1: Local LLM (Free, Fast)
- **Engine**: Ollama (GPU 0 - Titan RTX)
- **Model**: `deepseek-coder-v2:16b`
- **Cost**: $0.00 per request
- **Speed**: ~50-100 tokens/sec
- **Scope**: Handles 70-90% of queries
- **Routing**: Via `gravitas_supervisor` (Port 8000)

### L2: Network LLM (Economical)
- **Engine**: OpenRouter, Claude Haiku, Gemini Flash
- **Cost**: $0.001-0.003 per 1K tokens
- **Use Case**: Moderate complexity, low confidence from L1
- **Routing**: Auto-promoted when L1 VRAM < 2GB or confidence low

### L3: Premium Reasoning (High-cost, High-accuracy)
- **Engine**: Gemini 3 Pro (Vertex AI)
- **Cost**: $0.01-0.03 per 1K tokens
- **Use Case**: Strategic/creative tasks, cross-domain inference
- **Routing**: Manual or auto-promoted for complex queries

**Shared Infrastructure**:
- **RAG**: Qdrant (vector DB) - `data/qdrant/`
- **Object Store**: MinIO - `data/minio/`
- **History**: PostgreSQL - `data/postgres_data/`
- **Memory**: SQLite3 (`rag_memory.db`) - last 25 turns
- **Backend**: FastAPI (Python 3.12) - Port 5050

---

## 7. Microservices Topology

All services run in Docker containers:

| Service | Port | GPU | Purpose |
|---------|------|-----|---------|
| `gravitas_supervisor` | 8000 | - | L1/L2/L3 routing proxy |
| `gravitas_mcp` | 8001 | - | Main app (sleep infinity) |
| `Gravitas_ollama` | 11434 | GPU 0 | L1 model hosting |
| `Gravitas_ollama_embed` | 11435 | GPU 1 | Embeddings |
| `Gravitas_qdrant` | 6333 | - | Vector database |
| `Gravitas_minio` | 9000 | - | Object storage |
| `Gravitas_postgres` | 5432 | - | Chat history + telemetry |
| `Gravitas_lobby` | 5050 | - | Public API endpoint |

---

## 8. VRAM Protection & Circuit Breakers

### Overload Protection:
1. **Pre-flight Check**: `GPUtil` queries all GPUs before L1 inference
2. **Hard Limit**: If `Free_VRAM < 2GB`, request auto-promotes to L2
3. **History**: 60-day VRAM telemetry logged to Postgres
4. **Monitoring**: Supervisor tracks VRAM and routes intelligently

### Parallel Processing Benefits:
- Embeddings on GPU 1 don't block generation on GPU 0
- Frees ~6GB VRAM on Titan RTX for larger context windows
- GTX 1060 runs productive workloads vs idle display duty

---

## 9. Backup Configuration

### BorgBackup Repository:
- **Location**: `/mnt/f/dockerDesktopFromBorgeBackup/` (F: drive)
- **Source**: `/home/dflory/dev_env/Gravitas/`
- **Schedule**: Manual + optional cron (every 6 hours)
- **Retention**: 7 daily, 4 weekly, 6 monthly

### What's Backed Up:
✅ All code (`app/`, `tests/`, `docs/`)  
✅ **Model files** (`data/ollama_models/` - 22GB)  
✅ **Databases** (`data/postgres_data/`, `data/qdrant/`)  
✅ Config files (`docker-compose.yml`, `.env`)

### Deduplication:
- First backup: ~41GB
- Daily incremental: ~50-100MB (only changes)
- After 30 days: ~45GB total (not 1.2TB!)
- Models stored once, shared across all backups

---

## 10. Performance Characteristics

### Storage Performance:
- **C: (M.2 NVMe)**: ~3500 MB/s read, ~3000 MB/s write
- **Docker I/O**: Native ext4 (WSL2) - near-native Linux performance

### Inference Performance:
- **L1 (Titan RTX)**: 50-100 tokens/sec (deepseek-coder-v2:16b)
- **Embeddings (GTX 1060)**: ~1000 docs/sec (nomic-embed-text)

### VRAM Utilization:
- **Idle**: ~2GB (OS + drivers)
- **Model Loaded**: ~18GB (16GB model + overhead)
- **Safety Buffer**: 2GB minimum free
- **Max Context**: ~8K tokens with safety margin

---

## 11. Network Configuration

### Docker Network:
- **Name**: `Gravitas_net`
- **Type**: Bridge
- **All containers communicate via**: Internal DNS

### External Ports:
```
5050  → Gravitas_lobby (FastAPI)
8000  → gravitas_supervisor (Routing)
11434 → Gravitas_ollama (L1 Models)
11435 → Gravitas_ollama_embed (Embeddings)
6333  → Gravitas_qdrant (Vector DB)
9000  → Gravitas_minio (Object Store)
5432  → Gravitas_postgres (Database)
```

---

## 12. Quick Reference

### Access Gravitas Files:

**From WSL/Ubuntu**:
```bash
cd /home/dflory/dev_env/Gravitas
```

**From Windows PowerShell**:
```powershell
cd \\wsl.localhost\Ubuntu\home\dflory\dev_env\Gravitas
```

**From Windows Explorer**:
```
\\wsl.localhost\Ubuntu\home\dflory\dev_env\Gravitas
```

### Check Storage Usage:
```bash
# WSL filesystem
df -h /

# Gravitas data size
du -sh /home/dflory/dev_env/Gravitas/data/*

# Windows drives from WSL
df -h /mnt/c /mnt/d /mnt/f
```

### Check VRAM:
```bash
# From WSL
nvidia-smi

# Or via Docker
docker exec Gravitas_ollama nvidia-smi
```

---

**See Also**:
- `docs/004_hardware_operations.md` - Operational details
- `docs/BACKUP_SETUP.md` - Backup procedures
- `docs/007_model_governance.md` - L1/L2/L3 routing logic