# Gravitas Test Suite

Comprehensive test coverage for Gravitas v4.5.0 Grounded Research system.

## Quick Start

### Run All Specification Tests
```bash
python tests/run_spec_tests.py
```

### Run Specific Specification
```bash
python tests/run_spec_tests.py 001    # Core Architecture
python tests/run_spec_tests.py 006    # Telemetry Calibration
```

### Run Individual Test File
```bash
pytest tests/test_spec_001_core_architecture.py -v
pytest tests/test_telemetry.py -v
```

### List All Spec Tests
```bash
python tests/run_spec_tests.py --list
```

## Test Organization

### Specification Tests (00x Series)
These tests validate compliance with the 00x documentation series:

| File | Specification | Focus |
|:-----|:--------------|:------|
| `test_spec_001_core_architecture.py` | 001 | IoC Container, Driver Patterns, Reflex System |
| `test_spec_002_vector_memory.py` | 002 | Qdrant, Hybrid Search, Memory Hygiene |
| `test_spec_003_security_gatekeeper.py` | 003 | Safety Filter, Multi-Format Validation |
| `test_spec_004_hardware_operations.py` | 004 | Dual-GPU, VRAM Protection, Microservices |
| `test_spec_005_development_protocols.py` | 005 | TDD, SOLID, Version Control, Reasoning |
| `test_spec_006_telemetry_calibration.py` | 006 | Phase 4.5, Sub-Second Metrics, 60-Day Window |

### Feature Tests
Component-specific and integration tests:

- `test_telemetry.py` - Telemetry logging and aggregation
- `test_safety_logic.py` - Security gatekeeper validation
- `test_vram_safety.py` - VRAM overflow protection
- `test_hybrid_search.py` - Qdrant hybrid vector search
- `test_dual_gpu.py` - Dual-GPU architecture
- `test_memory_pruning.py` - Memory hygiene
- `test_nexus_api.py` - Dashboard API endpoints
- `test_integrated_rag_prompts.py` - End-to-end RAG testing
- And many more...

## Test Categories

### Unit Tests
Test individual components in isolation:
```bash
pytest tests/test_safety_logic.py -v
pytest tests/test_telemetry.py -v
```

### Integration Tests
Test component interactions:
```bash
pytest tests/test_integrated_rag_prompts.py -v
pytest tests/test_nexus_api.py -v
```

### Specification Compliance Tests
Validate adherence to architectural documentation:
```bash
python tests/run_spec_tests.py
```

## Test Dependencies

```bash
pip install pytest pytest-asyncio
```

## Writing New Tests

### Follow TDD Protocol (005_DEVELOPMENT_PROTOCOLS.md)

1. **Red:** Write failing test
2. **Green:** Implement minimal code to pass
3. **Refactor:** Clean up while keeping green

### Test File Naming

- Specification tests: `test_spec_00X_name.py`
- Feature tests: `test_feature_name.py`
- Integration tests: `test_integrated_name.py`

### Example Test Structure

```python
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.component import Component


class TestComponentFeature:
    """Test suite for specific feature"""
    
    def test_feature_exists(self):
        """Verify feature is implemented"""
        assert hasattr(Component, 'feature')
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test async operation"""
        result = await Component.async_method()
        assert result is not None
```

## Continuous Integration

### Exit Codes
- **0:** All tests passed
- **1:** One or more tests failed

### GitHub Actions Example
```yaml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Install dependencies
      run: pip install pytest pytest-asyncio
    - name: Run specification tests
      run: python tests/run_spec_tests.py
```

## Test Markers

Use pytest markers for conditional testing:

```python
@pytest.mark.asyncio              # Async test
@pytest.mark.skipif(condition)    # Conditional skip
@pytest.mark.slow                 # Long-running test
```

## Troubleshooting

### Database Tests Fail
Ensure Postgres container is running:
```bash
docker ps | grep postgres
```

### SKIP: Database not available
Normal in dev mode. Switch to RAG mode for full test coverage:
```bash
curl -X POST http://localhost:5050/system/mode -H "Content-Type: application/json" -d '{"mode":"RAG"}'
```

### Import Errors
Ensure you're running from project root:
```bash
cd /home/dflory/dev_env/Gravitas
python tests/run_spec_tests.py
```

## Documentation

- **Specifications:** `docs/00X_*.md`
- **Test Summary:** `docs/SPECIFICATION_TESTING_SUMMARY.md`
- **Phase 4.5 Summary:** `docs/PHASE_4.5_COMPLETION_SUMMARY.md`
- **Roadmap:** `docs/ROADMAP.md`

## Contributing

1. Write tests before implementation (TDD)
2. Ensure all specs tests pass before commit
3. Add integration tests for new features
4. Update documentation when changing architecture

---

**For detailed test coverage information, see:** `docs/SPECIFICATION_TESTING_SUMMARY.md`
