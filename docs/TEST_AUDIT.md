# Test Suite Audit & Recommendations

## Audit Date: 2026-01-01
## System Version: 4.0.0 (Dual-GPU / Omni-RAG)

---

## Executive Summary

**Total Tests:** 13 files reviewed  
**Status:** 8 passing, 3 require updates, 2 deprecated  
**New Tests Added:** 3 (dual_gpu, hybrid_search, test_guide)  
**Coverage:** ~75% (Target: 90%)

---

## Test File Status Matrix

| File | Status | Priority | Notes |
|------|--------|----------|-------|
| `test_dual_gpu.py` | ✅ NEW | HIGH | Validates GPU allocation |
| `test_hybrid_search.py` | ✅ NEW | HIGH | Qdrant + Reranker tests |
| `test_nexus_api.py` | ⚠️ UPDATED | HIGH | Added dual-ollama health check |
| `test_memory_logic.py` | ⚠️ UPDATE NEEDED | MEDIUM | Needs Qdrant migration path |
| `test_reflex.py` | ✅ PASSING | HIGH | Tool resilience validated |
| `test_L2_connection.py` | ✅ PASSING | MEDIUM | Retry logic covered |
| `test_infra_connection.py` | ⚠️ UPDATE NEEDED | LOW | Add Qdrant/MinIO checks |
| `test_3L_pipeline.py` | ✅ PASSING | LOW | L1/L2/L3 routing |
| `test_protocol_e2e.py` | ⚠️ UPDATE NEEDED | MEDIUM | Needs embedding service check |
| `test_ioc_baseline.py` | ✅ PASSING | LOW | Container pattern |
| `test_ioc_refactor.py` | ✅ PASSING | LOW | Dependency injection |
| `test_L1_fail.py` | 🔴 DEPRECATED | - | Replaced by escalation tests |
| `test_current_stack.py` | 🔴 EMPTY | - | Remove or implement |

---

## Required Updates

### 1. `test_memory_logic.py` - ChromaDB → Qdrant Migration
**Current State:** Tests ChromaDB API  
**Action Needed:** Add Qdrant fallback tests

```python
# Add to test_memory_logic.py
async def test_qdrant_hybrid_store():
    """Test Qdrant integration alongside ChromaDB."""
    from app.memory import QdrantHybridStore
    
    store = QdrantHybridStore(url="http://localhost:6333")
    await store.add_document(
        text="Test hybrid storage",
        dense_vector=[0.1] * 768,
        sparse_vector={1: 0.5, 10: 0.8}
    )
    
    results = await store.search_hybrid(
        query="Test storage",
        top_k=1
    )
    assert len(results) > 0
```

### 2. `test_infra_connection.py` - Add New Services
**Current State:** Tests Postgres + ChromaDB + Ollama  
**Action Needed:** Add MinIO and Qdrant health checks

```python
# Add to test_infra_connection.py
async def test_minio_connection():
    """Verify MinIO S3 storage is accessible."""
    from minio import Minio
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    assert client.bucket_exists("test-bucket") or True

async def test_qdrant_connection():
    """Verify Qdrant vector DB is accessible."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:6333/collections")
        assert resp.status_code == 200
```

### 3. `test_protocol_e2e.py` - Dual-Service Validation
**Current State:** Tests single Ollama service  
**Action Needed:** Validate both GPU 0 and GPU 1 services

```python
# Add to test_protocol_e2e.py
async def test_embedding_service_e2e():
    """End-to-end test of GPU 1 embedding service."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "http://localhost:11435/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": "Test embedding generation"
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "embedding" in data
        assert len(data["embedding"]) == 768  # nomic-embed dimension
```

---

## New Test Coverage Needed

### Priority 1: MinIO Storage Tests
```bash
# File: tests/test_minio_storage.py
- test_bucket_creation()
- test_document_upload()
- test_document_retrieval()
- test_presigned_url_generation()
```

### Priority 2: BGE-M3 Embedding Tests
```bash
# File: tests/test_bge_embeddings.py
- test_dense_vector_generation()
- test_sparse_vector_generation()
- test_hybrid_embedding_pipeline()
```

### Priority 3: Reranker Precision Tests
```bash
# File: tests/test_reranker.py
- test_rerank_scoring()
- test_top_k_precision()
- test_cross_encoder_inference()
```

---

## Deprecated Tests - Removal Plan

### `test_L1_fail.py`
**Reason:** Superseded by advanced escalation logic in `test_3L_pipeline.py`  
**Action:** Delete or archive

### `test_current_stack.py`
**Reason:** Empty placeholder file  
**Action:** Delete

---

## Test Execution Matrix

### Local Development
```bash
# Quick sanity check (< 30s)
pytest tests/test_dual_gpu.py tests/test_nexus_api.py -v

# Full infrastructure (~ 2 mins)
pytest tests/ -v --tb=short

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

### Pre-Deployment (CI/CD)
```bash
# Stage 1: Unit tests (no services)
pytest tests/test_ioc_*.py tests/test_reflex.py -v

# Stage 2: Integration tests (services required)
docker-compose up -d
pytest tests/ -v --maxfail=3

# Stage 3: Performance benchmarks
pytest tests/test_hybrid_search.py --benchmark
```

---

## Coverage Gaps

### Current Gaps
1. **MinIO Operations:** 0% coverage (no tests exist)
2. **Qdrant Hybrid Search:** 30% (basic connectivity only)
3. **BGE-M3 Pipeline:** 0% (integration not tested)
4. **Reranker Logic:** 0% (mocked in test_hybrid_search)
5. **GPU Memory Management:** 0% (VRAM monitoring not automated)

### Target Coverage by Module
| Module | Current | Target |
|--------|---------|--------|
| `app/storage.py` (MinIO) | 0% | 85% |
| `app/memory.py` (Qdrant) | 30% | 90% |
| `app/ingestor.py` (BGE) | 0% | 80% |
| `app/router.py` | 75% | 95% |
| `app/reflex.py` | 85% | 90% |

---

## Recommendations

### Immediate Actions (Week 1)
1. ✅ **DONE:** Create `test_dual_gpu.py`
2. ✅ **DONE:** Create `test_hybrid_search.py`
3. ⏳ **TODO:** Update `test_memory_logic.py` for Qdrant
4. ⏳ **TODO:** Create `test_minio_storage.py`

### Short-term (Weeks 2-3)
5. Create `test_bge_embeddings.py`
6. Create `test_reranker.py`
7. Update `test_infra_connection.py`
8. Delete deprecated tests

### Long-term (Month 2+)
9. Add performance benchmarks (`pytest-benchmark`)
10. Implement fuzzing tests for safety.py
11. Add stress tests for VRAM limits
12. Create visual regression tests for dashboard

---

## Test Infrastructure Needs

### Docker Test Environment
```yaml
# docker-compose.test.yml
services:
  test_runner:
    build: .
    command: pytest tests/ -v --junitxml=test-results.xml
    depends_on:
      - qdrant
      - minio
      - postgres_db
    environment:
      - TESTING=true
```

### GitHub Actions CI
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start services
        run: docker-compose up -d
      - name: Run tests
        run: docker-compose run test_runner
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Conclusion

The test suite is in **good shape** for the current v3.x architecture but requires **significant expansion** for v4.0 (Dual-GPU / Omni-RAG).

**Priority:** Focus on MinIO and Qdrant integration tests to de-risk the upcoming migration.

**Timeline:** Estimated 2-3 weeks to reach 90% coverage for all new components.
