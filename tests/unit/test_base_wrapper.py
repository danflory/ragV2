import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.wrappers.base_wrapper import GravitasAgentWrapper
from app.services.supervisor.guardian import AgentNotCertifiedError

# Concrete implementation for testing
class MockAgentWrapper(GravitasAgentWrapper):
    async def _execute_internal(self, task: Dict) -> Dict:
        self.pipe.log_thought("Thinking about " + task.get("prompt", ""))
        self.pipe.log_result("Success", {"tokens": 10})
        return {"output": "done"}

    def _parse_thought(self, chunk: Dict) -> Optional[str]:
        return chunk.get("thinking")

    def _parse_action(self, chunk: Dict) -> Optional[str]:
        return chunk.get("action")

@pytest.fixture
def mock_certs_dir(tmp_path):
    d = tmp_path / "certs"
    d.mkdir()
    
    # Create a valid certificate for 'MockAgent'
    cert_data = {
        "agent_name": "MockAgent",
        "issued_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "signature": "mock",
        "version": "1.0"
    }
    (d / "MockAgent.json").write_text(json.dumps(cert_data))
    return d

@pytest.mark.asyncio
async def test_execute_task_flow(mock_certs_dir, monkeypatch):
    # Mock journals directory as well
    journals_dir = mock_certs_dir / "journals"
    journals_dir.mkdir()
    
    # Mock Path.mkdir and journaling paths in ReasoningPipe
    from app.lib.reasoning_pipe import ReasoningPipe
    def mock_pipe_init(self, agent_name, session_id, model, tier):
        self.agent_name = agent_name
        self.session_id = session_id
        self.model = model
        self.tier = tier
        self.start_time = datetime.now()
        self.buffer = []
        self.metrics = {"tokens": 0, "duration": 0.0, "cost": 0.0, "tokens_per_second": 0.0}
        self.task_description = None
        self.is_finalized = False
        self.journals_dir = journals_dir
        self.output_path = self.journals_dir / f"ReasoningPipe_{agent_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"ReasoningPipe_{agent_name}.md"
    
    monkeypatch.setattr(ReasoningPipe, "__init__", mock_pipe_init)

    # Monkeypatch SupervisorGuardian to use our temp certs dir
    from app.services.supervisor.guardian import SupervisorGuardian
    original_init = SupervisorGuardian.__init__
    def mock_guardian_init(self, certificates_dir=str(mock_certs_dir)):
        original_init(self, certificates_dir=certificates_dir)
    
    monkeypatch.setattr(SupervisorGuardian, "__init__", mock_guardian_init)

    wrapper = MockAgentWrapper("MockAgent", "sess_TEST", "mock-model", "L1")
    result = await wrapper.execute_task({"prompt": "Hello"})
    
    assert result == {"output": "done"}
    assert (journals_dir / "ReasoningPipe_MockAgent_sess_TEST.md").exists()

@pytest.mark.asyncio
async def test_execute_task_rejection(mock_certs_dir, monkeypatch):
    from app.services.supervisor.guardian import SupervisorGuardian
    original_init = SupervisorGuardian.__init__
    def mock_guardian_init(self, certificates_dir=str(mock_certs_dir)):
        original_init(self, certificates_dir=certificates_dir)
    monkeypatch.setattr(SupervisorGuardian, "__init__", mock_guardian_init)

    # Agent 'UncertifiedAgent' has no certificate in mock_certs_dir
    wrapper = MockAgentWrapper("UncertifiedAgent", "sess_FAIL", "mock-model", "L1")
    
    with pytest.raises(AgentNotCertifiedError):
        await wrapper.execute_task({"prompt": "Hello"})

def test_abstract_methods():
    # Attempting to instantiate ABC without methods should fail
    class IncompleteWrapper(GravitasAgentWrapper):
        pass
    
    with pytest.raises(TypeError):
        IncompleteWrapper("Test", "sess", "model", "L1")
