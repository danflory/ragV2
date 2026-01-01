# AntiGravity RAG - Dual-GPU Architecture Specification
**Version:** 4.0.0 (Omni-RAG / Dual-GPU / Production-Scale)  
**Updated:** 2026-01-01  
**Hardware:** Dual NVIDIA GPUs (Titan RTX 24GB + GTX 1060 6GB)

## 1. Executive Summary

The AntiGravity RAG has evolved into a **Production-Grade Hybrid RAG Architecture** optimized for processing thousands of pages with precision retrieval. The system now leverages **dual NVIDIA GPUs** for parallel processing and implements **Dense + Sparse hybrid vector search** via Qdrant.

### Key Upgrades (v4.0)
- **Dual-GPU Architecture**: Titan RTX for generation, GTX 1060 for embeddings
- **Hybrid Vector Search**: Dense (semantic) + Sparse (lexical) via BGE-M3
- **Object Storage**: MinIO for raw document persistence
- **Advanced Reranking**: BGE-Reranker for precision hits
- **27B Parameter Model**: Gemma-2-27B-Instruct (Q4_K_M) for superior reasoning

---

## 2. Hardware Architecture

### GPU 0: NVIDIA Titan RTX (24GB VRAM)
**Role:** Primary Compute / Generation  
**Services:** `agy_ollama` (Port 11434)  
**Models:**
- `gemma2:27b-instruct-q4_k_m` (~17GB VRAM)
- **Context Headroom:** +7GB for extended conversations

**Environment:**
```yaml
CUDA_VISIBLE_DEVICES: 0
device_ids: ['0']
```

### GPU 1: NVIDIA GeForce GTX 1060 (6GB VRAM)
**Role:** Dedicated Embedding Engine  
**Services:** `agy_ollama_embed` (Port 11435)  
**Models:**
- `nomic-embed-text-v1.5` (~1.5GB VRAM)
- `BAAI/bge-m3` (Dense+Sparse) (~2GB VRAM)  
- `BAAI/bge-reranker-v2-m3` (~1GB VRAM)

**Environment:**
```yaml
CUDA_VISIBLE_DEVICES: 1
device_ids: ['1']
```

**Benefits:**
- **Parallel Processing**: Embeddings don't block generation
- **VRAM Optimization**: Frees 6-7GB on Titan RTX for larger context
- **Cost Efficiency**: GTX 1060 runs productive workloads instead of idle display duty

---

## 3. Multi-Layer Cognitive Pipeline

### L1 (Reflex - Local)
**Model:** `gemma2:27b-instruct-q4_k_m`  
**Host:** GPU 0 (Titan RTX)  
**Response Time:** <2s  
**Use Cases:** Chat, code completion, routine queries

### L2 (Reasoning - Cloud)
**Model:** `Qwen2.5-Coder-32B-Instruct` (DeepInfra)  
**Retry Logic:** 3 attempts with exponential backoff  
**Use Cases:** Complex refactoring, architectural decisions  
**Trigger:** `\L2` command or automatic escalation

### L3 (Agentic - Research)
**Model:** `gemini-3-pro-preview` (Google)  
**Status:** Configured (Dormant)  
**Use Cases:** Multi-step research, long-form synthesis

---

## 4. Hybrid RAG Architecture

### 4.1 Storage Layer
**MinIO (S3-Compatible Object Storage)**
- Port: 9000 (API), 9001 (Console)
- Purpose: Raw document persistence (PDFs, markdown, code)
- Volume: `./data/minio`

### 4.2 Vector Database
**Qdrant (Hybrid Search Engine)**
- Port: 6333 (HTTP API)
- Capabilities:
  - **Dense Vectors** (1024d): Semantic concept matching
  - **Sparse Vectors** (Lexical): Exact keyword matching ("King of Hits")
- Volume: `./data/qdrant`

### 4.3 Embedding Pipeline

#### Stage 1: Dual Embedding
```python
# nomic-embed-text-v1.5 (GPU 1)
dense_vector = embed_nomic(chunk)  # 768d semantic

# BAAI/bge-m3 (GPU 1)
sparse_vector = embed_bge_m3(chunk)  # Lexical keywords
```

#### Stage 2: Retrieval
```python
# Qdrant Hybrid Search
results = qdrant.search_hybrid(
    query_dense=query_embedding,
    query_sparse=query_keywords,
    top_k=10
)
```

#### Stage 3: Reranking
```python
# BAAI/bge-reranker-v2-m3 (GPU 1)
ranked = reranker.score(query, results)
top_3 = ranked[:3]  # Precision hits
```

---

## 5. Docker Services

### Service Matrix
| Service | Container | GPU | Port | Purpose |
|---------|-----------|-----|------|---------|
| `rag_app` | `agy_rag_backend` | 0 | 5050 | API + Orchestration |
| `ollama` | `agy_ollama` | 0 | 11434 | Generation (Gemma-2-27B) |
| `ollama_embed` | `agy_ollama_embed` | 1 | 11435 | Embeddings (Nomic/BGE) |
| `qdrant` | `agy_qdrant` | - | 6333 | Vector DB |
| `minio` | `agy_minio` | - | 9000/9001 | Object Storage |
| `postgres_db` | `agy_postgres` | - | 5432 | Chat History |

---

## 6. Application Structure

```
/rag_local
├── app/
│   ├── main.py              # Entry Point (Uvicorn)
│   ├── router.py            # API Routes + L2 Retry Logic
│   ├── container.py         # IoC Switchboard
│   ├── storage.py           # MinIO SDK (Object Storage)
│   ├── memory.py            # Qdrant Hybrid Search + Reranker
│   ├── ingestor.py          # BGE-M3 Hybrid Embedding Pipeline
│   ├── reflex.py            # Shell/Git + Tool Resilience
│   ├── safety.py            # Gatekeeper (Command Validation)
│   ├── database.py          # Postgres (Chat History + Stats)
│   ├── L1_local.py          # Gemma-2-27B Driver
│   ├── L2_network.py        # DeepInfra Driver (Retry Logic)
│   └── config.py            # Pydantic Settings
├── dashboard/
│   ├── index.html           # Nexus UI (Muted Dark Mode)
│   ├── app.js               # Frontend Logic + Markdown Rendering
│   └── style.css            # Shadow Works Aesthetic
├── data/
│   ├── ollama_models/       # GPU 0 Models
│   ├── ollama_embed_models/ # GPU 1 Models
│   ├── qdrant/              # Vector DB Storage
│   ├── minio/               # Object Storage
│   └── postgres_data/       # SQL History
├── tests/
│   ├── test_dual_gpu.py     # GPU allocation verification
│   ├── test_hybrid_search.py # Qdrant retrieval tests
│   └── test_reranker.py     # BGE-Reranker precision tests
├── docker-compose.yml       # Infrastructure Orchestration
└── requirements.txt         # Python Dependencies
```

---

## 7. Security & Resilience

### 7.1 Gatekeeper Protocol
- **Command Validation:** `safety.py` blocks dangerous shell commands
- **Secret Scanning:** Prevents API key leakage
- **Git Auth Resilience:** Graceful handling of headless container auth failures

### 7.2 Tool Resilience
- **Cloud CLI Detection:** Intercepts missing `bq`/`gcloud` commands
- **Guidance:** Provides Python SDK alternatives

### 7.3 L2 Network Resilience
- **Exponential Backoff:** 3 retries (1s, 2s, 4s delays)
- **Smart Failure:** 4xx errors fail fast, 5xx errors retry
- **Clean Errors:** Sanitized messages for user-facing UI

---

## 8. Development Protocols

### 8.1 TDD & SOLID
- **Test-First:** Generate failing tests before implementation
- **Single Responsibility:** Each module has one job
- **Dependency Injection:** `container.py` is source of truth

### 8.2 Code Quality
- **Linting:** `ruff` enforced
- **Formatting:** `black` auto-applied
- **Type Safety:** Pydantic models for all configs

### 8.3 Git Hygiene
- **Atomic Commits:** Small, frequent updates
- **Gatekeeper Approval:** All reflexes validated before execution

---

## 9. Performance Benchmarks

### VRAM Distribution
| Component | GPU | VRAM Usage |
|-----------|-----|------------|
| Gemma-2-27B-Q4_K_M | 0 | ~17GB |
| Context Buffer | 0 | ~5-7GB |
| **Total (GPU 0)** | **0** | **~22-24GB** |
| Nomic-Embed | 1 | ~1.5GB |
| BGE-M3 | 1 | ~2GB |
| BGE-Reranker | 1 | ~1GB |
| **Total (GPU 1)** | **1** | **~4.5GB** |

### Retrieval Performance
- **Dense Search:** ~50ms for 10k chunks
- **Sparse Search:** ~20ms for exact keywords
- **Reranking:** ~30ms for top-10 results
- **Total Latency:** <200ms end-to-end

---

## 10. Future Enhancements

- **Knowledge Graph:** Neo4j for entity relationships
- **Multi-Modal:** Image + PDF OCR ingestion
- **Streaming Responses:** SSE for real-time generation
- **A/B Testing:** Compare retrieval strategies
- **Auto-Tuning:** Dynamic chunk size optimization
