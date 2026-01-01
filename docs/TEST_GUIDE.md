# Test Execution Guide

## Overview
This guide covers running the AntiGravity RAG test suite, which validates the dual-GPU architecture, hybrid search capabilities, and API endpoints.

## Test Categories

### 1. Infrastructure Tests
**File:** `test_dual_gpu.py`  
**Purpose:** Validate GPU allocation and service isolation

```bash
# Run dual-GPU tests
pytest tests/test_dual_gpu.py -v

# Or run standalone
python tests/test_dual_gpu.py
```

**Checks:**
- GPU 0 (Titan RTX) running generation service on port 11434
- GPU 1 (GTX 1060) running embedding service on port 11435
- Parallel processing capability
- VRAM isolation

### 2. Hybrid Search Tests
**File:** `test_hybrid_search.py`  
**Purpose:** Validate Qdrant Dense+Sparse retrieval

```bash
# Run hybrid search tests
pytest tests/test_hybrid_search.py -v

# Requires Qdrant running
docker-compose up -d qdrant
```

**Checks:**
- Qdrant connection (port 6333)
- Hybrid collection creation (Dense + Sparse vectors)
- Point upsert and retrieval
- Dense semantic search
- Reranker integration (mock)

### 3. API Tests
**File:** `test_nexus_api.py`  
**Purpose:** Validate core API endpoints

```bash
# Run API tests
pytest tests/test_nexus_api.py -v
```

**Checks:**
- `/health/detailed` - Service health status
- `/stats/summary` - Usage statistics
- CORS headers
- Model pull endpoint

### 4. Memory Tests
**File:** `test_memory_logic.py`  
**Purpose:** Validate hybrid memory (Chroma + Postgres)

```bash
# Run memory tests
python tests/test_memory_logic.py
```

**Checks:**
- ChromaDB vector storage
- Postgres short-term history
- Round-trip persistence

### 5. Reflex Tests
**File:** `test_reflex.py`  
**Purpose:** Validate shell execution and safety

```bash
# Run reflex tests
pytest tests/test_reflex.py -v
```

**Checks:**
- Command validation (Gatekeeper)
- Git sync operations
- Tool resilience (bq/gcloud missing)

## Running All Tests

```bash
# Run entire suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_dual_gpu.py::test_gpu0_ollama_service -v
```

## Pre-Test Checklist

### Services Must Be Running
```bash
# Start all services
docker-compose up -d

# Verify status
docker-compose ps

# Expected services:
# - agy_rag_backend (port 5050)
# - agy_ollama (port 11434, GPU 0)
# - agy_ollama_embed (port 11435, GPU 1)
# - agy_qdrant (port 6333)
# - agy_minio (ports 9000, 9001)
# - agy_postgres (port 5432)
```

### Models Must Be Pulled
```bash
# GPU 0: Generation models
docker exec agy_ollama ollama pull gemma2:27b

# GPU 1: Embedding models
docker exec agy_ollama_embed ollama pull nomic-embed-text
# Note: bge-m3 and bge-reranker pulled via Python SDK
```

## Test Data Cleanup

```bash
# Remove test collections
docker exec agy_qdrant rm -rf /qdrant/storage/collections/test_*

# Clear test PostgreSQL history
docker exec agy_postgres psql -U agy_user -d chat_history -c "DELETE FROM history WHERE content LIKE '%test%';"
```

## Continuous Integration

Future CI pipeline (GitHub Actions):
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build containers
        run: docker-compose up -d
      - name: Run tests
        run: docker-compose exec rag_app pytest tests/ -v
```

## Test Coverage Goals

- **Infrastructure:** 100% (GPU allocation, service health)
- **API:** 95% (all endpoints except admin)
- **Memory:** 90% (RAG pipeline, persistence)
- **Reflex:** 85% (safety checks, edge cases)

## Troubleshooting

### Test Fails: "Connection Refused"
```bash
# Check service is running
docker-compose ps
docker-compose logs agy_ollama

# Restart service
docker-compose restart agy_ollama
```

### Test Fails: "Model Not Found"
```bash
# List available models
docker exec agy_ollama ollama list

# Pull missing model
docker exec agy_ollama ollama pull <model_name>
```

### Test Fails: "CUDA Out of Memory"
```bash
# Check VRAM usage
nvidia-smi

# Restart services to clear VRAM
docker-compose restart
```
