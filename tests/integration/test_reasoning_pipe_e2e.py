import pytest
import asyncio
import os
import shutil
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, AsyncMock

from app.services.supervisor.certifier import WrapperCertifier
from app.services.supervisor.guardian import SupervisorGuardian, AgentNotCertifiedError, CertificationExpiredError
from app.wrappers.base_wrapper import GravitasAgentWrapper
from app.lib.reasoning_pipe import ReasoningPipe

# --- Helpers ---

class IntegrationMockWrapper(GravitasAgentWrapper):
    """A real-ish wrapper for E2E testing that doesn't call real APIs."""
    def __init__(self, session_id: str, model_name: str = "integration-mock"):
        super().__init__(
            ghost_name="IntegrationAgent",
            session_id=session_id,
            model=model_name,
            tier="L1"
        )
    
    async def _execute_internal(self, task: dict) -> dict:
        self.pipe.log_thought("Beginning integration test task.")
        await asyncio.sleep(0.1) # Simulate some work
        self.pipe.log_action("IntegrationAction", {"step": 1})
        self.pipe.log_result("Success", metrics={"tokens": 50})
        return {"output": "Mock integration result"}

    def _parse_thought(self, chunk: dict): return None
    def _parse_action(self, chunk: dict): return None

# --- Fixtures ---

@pytest.fixture
def e2e_env(tmp_path):
    # Setup test directories
    certs_dir = tmp_path / "certs"
    journals_dir = tmp_path / "journals"
    certs_dir.mkdir()
    journals_dir.mkdir()
    
    # Store original env vars if any
    
    yield certs_dir, journals_dir
    
    # Cleanup is handled by tmp_path

# --- Tests ---

@pytest.mark.asyncio
async def test_full_certification_workflow(e2e_env):
    certs_dir, journals_dir = e2e_env
    
    # Create a wrapper file for certification
    wrapper_code = """
from app.wrappers.base_wrapper import GravitasAgentWrapper
from typing import Optional, Dict

class ValidIntegrationWrapper(GravitasAgentWrapper):
    def __init__(self, session_id: str = "test", model_name: str = "test"):
        super().__init__(ghost_name="IntegrationAgent", session_id=session_id, model=model_name, tier="L1")
    async def _execute_internal(self, task: Dict) -> Dict:
        self.pipe.log_thought("Thinking...")
        self.pipe.log_result("Success")
        return {"output": "ok"}
    def _parse_thought(self, chunk: Dict) -> Optional[str]: return None
    def _parse_action(self, chunk: Dict) -> Optional[str]: return None
"""
    wrapper_path = journals_dir.parent / "integration_wrapper.py"
    wrapper_path.write_text(wrapper_code)
    
    certifier = WrapperCertifier(certificates_dir=str(certs_dir))
    
    # 1. Certify wrapper
    # We patch SupervisorGuardian inside certify_wrapper to use our test certs dir
    with patch("app.services.supervisor.certifier.SupervisorGuardian") as MockGuardian:
        mock_guardian_instance = MockGuardian.return_value
        mock_guardian_instance.notify_session_start.return_value = type('Perm', (), {'allowed': True})()
        
        # Override the journals_dir in the dynamic instance during test
        with patch("app.lib.reasoning_pipe.Path", side_effect=lambda x: journals_dir if x == "docs/journals" else Path(x)):
             result = await certifier.certify_wrapper(str(wrapper_path), "IntegrationAgent")
    
    assert result.passed is True
    assert (certs_dir / "IntegrationAgent.json").exists()
    
    # 2. Execute task with the certified wrapper
    # We need to instantiate the wrapper and point it to the right guardian
    from app.services.supervisor.guardian import SupervisorGuardian
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    # We'll use our local IntegrationMockWrapper but with the certificate we just created
    # and we need to ensure it uses the same guardian instance
    wrapper = IntegrationMockWrapper(session_id="session_e2e_1")
    wrapper.supervisor = guardian
    # Point pipe to test journals
    wrapper.pipe.journals_dir = journals_dir
    wrapper.pipe.output_path = journals_dir / f"{wrapper.ghost_name}_{wrapper.session_id}.md"
    wrapper.pipe.summary_path = journals_dir / f"{wrapper.ghost_name}_journal.md"
    
    await wrapper.execute_task({"prompt": "E2E Test"})
    
    # 3. Verify pipe creation and tracking
    assert wrapper.pipe.output_path.exists()
    content = wrapper.pipe.output_path.read_text()
    assert "IntegrationAction" in content
    
    stats = guardian.get_session_stats("IntegrationAgent")
    assert stats["IntegrationAgent"]["completed_total"] == 1

@pytest.mark.asyncio
async def test_multi_agent_concurrent_execution(e2e_env):
    certs_dir, journals_dir = e2e_env
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    # Create certs for two agents
    for agent in ["AgentA", "AgentB"]:
        cert_data = {
            "agent_name": agent,
            "issued_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "signature": "mock",
            "version": "1.0"
        }
        with open(certs_dir / f"{agent}.json", "w") as f:
            json.dump(cert_data, f)
    
    # Reload guardian to see new certs
    guardian.certified_agents = guardian._load_certificates()
    
    async def run_agent(name, sess_id):
        wrapper = IntegrationMockWrapper(session_id=sess_id)
        wrapper.ghost_name = name
        wrapper.supervisor = guardian
        wrapper.pipe.ghost_name = name
        wrapper.pipe.journals_dir = journals_dir
        wrapper.pipe.output_path = journals_dir / f"{name}_{sess_id}.md"
        wrapper.pipe.summary_path = journals_dir / f"{name}_journal.md"
        return await wrapper.execute_task({"prompt": f"Task for {name}"})

    # Run simultaneously
    results = await asyncio.gather(
        run_agent("AgentA", "sess_A"),
        run_agent("AgentB", "sess_B")
    )
    
    assert len(results) == 2
    assert (journals_dir / "AgentA_sess_A.md").exists()
    assert (journals_dir / "AgentB_sess_B.md").exists()
    
    stats = guardian.get_session_stats()
    assert stats["AgentA"]["completed_total"] == 1
    assert stats["AgentB"]["completed_total"] == 1

@pytest.mark.asyncio
async def test_uncertified_agent_rejection(e2e_env):
    certs_dir, _ = e2e_env
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    wrapper = IntegrationMockWrapper(session_id="sess_reject")
    wrapper.supervisor = guardian
    
    with pytest.raises(AgentNotCertifiedError):
        await wrapper.execute_task({"prompt": "should fail"})

@pytest.mark.asyncio
async def test_expired_certificate_rejection(e2e_env):
    certs_dir, _ = e2e_env
    
    # Create expired cert
    cert_data = {
        "agent_name": "IntegrationAgent",
        "issued_at": (datetime.now() - timedelta(days=40)).isoformat(),
        "expires_at": (datetime.now() - timedelta(days=10)).isoformat(),
        "signature": "mock"
    }
    with open(certs_dir / "IntegrationAgent.json", "w") as f:
        json.dump(cert_data, f)
        
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    wrapper = IntegrationMockWrapper(session_id="sess_expired")
    wrapper.supervisor = guardian
    
    with pytest.raises(CertificationExpiredError):
        await wrapper.execute_task({"prompt": "should fail"})

@pytest.mark.asyncio
async def test_performance_overhead(e2e_env):
    certs_dir, journals_dir = e2e_env
    
    # Create valid cert
    cert_data = {
        "agent_name": "IntegrationAgent",
        "issued_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "signature": "mock"
    }
    with open(certs_dir / "IntegrationAgent.json", "w") as f:
        json.dump(cert_data, f)
        
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    # Baseline: Just the internal logic
    start_baseline = time.perf_counter()
    for _ in range(10):
        # Match sleep in IntegrationMockWrapper
        await asyncio.sleep(0.1)
    baseline_dur = time.perf_counter() - start_baseline
    
    # With ReasoningPipe overhead
    wrapper = IntegrationMockWrapper(session_id="perf_test")
    wrapper.supervisor = guardian
    wrapper.pipe.journals_dir = journals_dir
    
    # We'll run it 10 times to average out noise
    start_pipe = time.perf_counter()
    for i in range(10):
        # Important: Fresh session for each execution to avoid finalization warnings/errors
        wrapper.session_id = f"perf_{i}"
        wrapper.pipe.session_id = f"perf_{i}"
        wrapper.pipe.output_path = journals_dir / f"perf_{i}.md"
        wrapper.pipe.summary_path = journals_dir / f"summary_perf.md"
        wrapper.pipe.start_time = datetime.now()
        wrapper.pipe.is_finalized = False
        wrapper.pipe.buffer = []
        
        await wrapper.execute_task({"prompt": "overhead test"})
    pipe_dur = time.perf_counter() - start_pipe
    
    overhead = (pipe_dur - baseline_dur) / baseline_dur
    print(f"Baseline: {baseline_dur:.4f}s, With Pipe: {pipe_dur:.4f}s, Overhead: {overhead:.2%}")
    # Assert that overhead is reasonably small. 
    # CI environments can be noisy, but it should definitely be within 10% for these light tasks.
    assert pipe_dur < baseline_dur * 1.10
