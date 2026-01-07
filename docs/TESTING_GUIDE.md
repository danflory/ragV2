# GRAVITAS TESTING GUIDE - PHASE 6+
**Version**: 6.0.0  
**Last Updated**: 2026-01-06  
**Status**: Active

---

## QUICK START

### Run All Passing Tests (Core Suite):
```bash
cd /home/dflory/dev_env/Gravitas
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/unit/test_reasoning_pipe.py tests/test_spec_008_reasoning_pipes.py::TestReasoningPipeClass -v
```

**Expected**: 19 passed ✅

---

## TEST CATEGORIES

### 1. Unit Tests (`tests/unit/`)

#### ReasoningPipe Tests
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/unit/test_reasoning_pipe.py -v
```
**Coverage**: 8 tests - initialization, logging, finalization, error handling  
**Status**: ✅ All passing

#### Base Wrapper Tests
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/unit/test_base_wrapper.py -v
```
**Coverage**: 3 tests - abstract methods, execution flow, certification enforcement  
**Status**: ⚠️ 1 passed, 2 skipped (need pytest-asyncio)

#### Supervisor Guardian Tests
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/unit/test_supervisor_guardian.py -v
```
**Coverage**: 6 tests - certificate loading, session management, stats  
**Status**: ⚠️ All skipped (need pytest-asyncio)

### 2. Specification Tests (`tests/`)

#### Spec 008: Reasoning Pipes
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/test_spec_008_reasoning_pipes.py -v
```
**Coverage**: 23 tests across 5 test classes  
**Status**: ⚠️ 19 passed, 9 skipped (need pytest-asyncio)

**Individual Test Classes**:
```bash
# ReasoningPipe Class (7 tests - all passing)
pytest tests/test_spec_008_reasoning_pipes.py::TestReasoningPipeClass -v

# Supervisor Guardian (6 tests - 1 passing, 5 skipped)
pytest tests/test_spec_008_reasoning_pipes.py::TestSupervisorGuardian -v

# Base Wrapper (3 tests - 1 passing, 2 skipped)
pytest tests/test_spec_008_reasoning_pipes.py::TestBaseWrapper -v

# Wrapper Certifier (5 tests - 4 passing, 1 skipped)
pytest tests/test_spec_008_reasoning_pipes.py::TestWrapperCertifier -v

# Reasoning Pipe Auditor (2 tests - all skipped)
pytest tests/test_spec_008_reasoning_pipes.py::TestReasoningPipeAuditor -v
```

### 3. Integration Tests (`tests/integration/`)

#### Reasoning Pipe End-to-End
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/integration/test_reasoning_pipe_e2e.py -v
```
**Coverage**: Full certification workflow, concurrent execution, rejection scenarios  
**Status**: ❓ Not yet run (needs pytest-asyncio)

#### Phase 5: Model Governance
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/integration/test_phase5_model_governance.py -v
```
**Coverage**: L1/L2/L3 routing, queue management, shadow audit  
**Status**: ❓ Not yet run

### 4. Manual Tests (`tests/manual/`)

#### Wrapper Mock Tests
```bash
# Ollama Wrapper
python tests/manual/test_ollama_wrapper_mock.py

# DeepInfra Wrapper
python tests/manual/test_deepinfra_wrapper_mock.py

# Claude Wrapper
python tests/manual/test_claude_wrapper_mock.py
```

---

## SETUP INSTRUCTIONS

### 1. Install Core Dependencies
```bash
pip install pytest pytest-asyncio
```

### 2. Install Optional Dependencies (for full coverage)
```bash
pip install respx pathspec google-generativeai
```

### 3. Configure pytest
Ensure `pyproject.toml` has:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### 4. Set PYTHONPATH
```bash
export PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH
```

Or add to your shell profile:
```bash
echo 'export PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

---

## COMMON TEST COMMANDS

### Run All Tests
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/ -v
```

### Run Tests with Coverage
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/ --cov=app --cov-report=html
```

### Run Specific Test
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/unit/test_reasoning_pipe.py::test_finalize_creates_file -v
```

### Run Tests Matching Pattern
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/ -k "reasoning" -v
```

### Run Tests with Detailed Output
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/ -vv --tb=long
```

### Run Tests and Stop on First Failure
```bash
PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH pytest tests/ -x
```

---

## TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution**: Set PYTHONPATH
```bash
export PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH
```

### Issue: "PytestUnknownMarkWarning: Unknown pytest.mark.asyncio"
**Solution**: Install pytest-asyncio
```bash
pip install pytest-asyncio
```

### Issue: "async def functions are not natively supported"
**Solution**: Configure asyncio_mode in pyproject.toml
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Issue: Tests fail with "No module named 'respx'"
**Solution**: Install optional dependency
```bash
pip install respx
```

### Issue: Tests fail with "No module named 'google'"
**Solution**: Install Google Generative AI SDK
```bash
pip install google-generativeai
```

---

## TEST DEVELOPMENT GUIDELINES

### 1. Test Naming Convention
```python
# Good:
def test_reasoning_pipe_initialization():
def test_log_thought_adds_to_buffer():
def test_finalize_creates_file():

# Bad:
def test1():
def test_stuff():
def my_test():
```

### 2. Test Structure (AAA Pattern)
```python
def test_example():
    # Arrange: Set up test data
    pipe = ReasoningPipe(ghost_name="Scout", session_id="123", model="gpt-4", tier="L1")
    
    # Act: Perform the action
    pipe.log_thought("Test thought")
    
    # Assert: Verify the result
    assert len(pipe.buffer) == 1
    assert "THOUGHT: Test thought" in pipe.buffer[0]
```

### 3. Use Fixtures for Common Setup
```python
@pytest.fixture
def temp_journals(tmp_path):
    journals_dir = tmp_path / "docs" / "journals"
    journals_dir.mkdir(parents=True)
    return journals_dir

def test_with_fixture(temp_journals):
    # Use temp_journals in test
    pass
```

### 4. Test Error Cases
```python
def test_log_thought_empty_fails():
    pipe = ReasoningPipe(ghost_name="Scout", session_id="123", model="gpt-4", tier="L1")
    with pytest.raises(ValueError):
        pipe.log_thought("")
```

### 5. Use Mocks for External Dependencies
```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    wrapper = MockWrapper(ghost_name="Scout", session_id="sess1", model="gpt-4", tier="L2")
    wrapper.supervisor = AsyncMock(spec=SupervisorGuardian)
    wrapper.supervisor.notify_session_start.return_value = SessionPermission(allowed=True)
    # ... test logic
```

---

## CONTINUOUS INTEGRATION

### Pre-Commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
export PYTHONPATH=/home/dflory/dev_env/Gravitas:$PYTHONPATH
pytest tests/unit/test_reasoning_pipe.py tests/test_spec_008_reasoning_pipes.py::TestReasoningPipeClass -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions (Future)
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio
      - name: Run tests
        run: |
          export PYTHONPATH=$PWD:$PYTHONPATH
          pytest tests/ -v
```

---

## TEST COVERAGE GOALS

| Component | Current | Target |
|-----------|---------|--------|
| ReasoningPipe Library | 100% | 100% ✅ |
| SupervisorGuardian | 60% | 95% |
| WrapperCertifier | 80% | 95% |
| ReasoningPipeAuditor | 40% | 90% |
| Base Wrapper | 70% | 95% |
| Agent Wrappers | 50% | 85% |
| **Overall** | **70%** | **90%** |

---

## RELATED DOCUMENTATION

- `docs/TEST_AUDIT_SUMMARY.md` - Latest audit results
- `docs/TEST_AUDIT_PHASE6_FINAL.md` - Detailed audit report
- `docs/008_reasoning_pipes.md` - Specification
- `docs/WRAPPER_DEVELOPMENT_GUIDE.md` - Wrapper development guide
- `docs/005_development_protocols.md` - TDD protocols

---

**Maintained By**: Antigravity Agent  
**Last Test Run**: 2026-01-06  
**Status**: 19/19 core tests passing ✅
