import pytest
from pathlib import Path
from datetime import datetime
from app.lib.reasoning_pipe import ReasoningPipe, ReasoningPipeWriteError
import os
import shutil

@pytest.fixture
def temp_journals(tmp_path):
    # Mocking the docs/journals directory for testing
    journals_dir = tmp_path / "docs" / "journals"
    journals_dir.mkdir(parents=True)
    return journals_dir

def test_reasoning_pipe_initialization():
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    assert pipe.ghost_name == "test_agent"
    assert pipe.agent_name == "test_agent"  # Backward compatibility alias
    assert pipe.session_id == "sess_123"
    assert pipe.model == "gpt-4"
    assert pipe.tier == "L1"
    assert pipe.is_finalized is False
    assert len(pipe.buffer) == 0

def test_log_thought():
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    pipe.log_thought("Thinking about life")
    assert len(pipe.buffer) == 1
    assert "THOUGHT: Thinking about life" in pipe.buffer[0]

def test_log_thought_empty_fails():
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    with pytest.raises(ValueError):
        pipe.log_thought("")

def test_log_action():
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    pipe.log_action("search", {"query": "test"})
    assert len(pipe.buffer) == 1
    assert "ACTION: search (query: test)" in pipe.buffer[0]

def test_log_result():
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    pipe.log_result("Success", {"tokens": 100, "cost": 0.05})
    assert len(pipe.buffer) == 1
    assert "RESULT: Success" in pipe.buffer[0]
    assert pipe.metrics["tokens"] == 100
    assert pipe.metrics["cost"] == 0.05

def test_finalize_creates_file(tmp_path, monkeypatch):
    # Change CWD or mock journals_dir to tmp_path
    journals_dir = tmp_path / "docs" / "journals"
    journals_dir.mkdir(parents=True)
    
    # Simple monkeypatch to point journals_dir to our temp one
    def mock_init(self, ghost_name, session_id, model, tier, agent_name=None):
        self.ghost_name = ghost_name
        self.agent_name = ghost_name  # Backward compatibility
        self.session_id = session_id
        self.model = model
        self.tier = tier
        self.start_time = datetime.now()
        self.buffer = []
        self.metrics = {"tokens": 0, "duration": 0.0, "cost": 0.0, "tokens_per_second": 0.0}
        self.task_description = None
        self.is_finalized = False
        self.journals_dir = journals_dir
        self.output_path = self.journals_dir / f"{ghost_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"{ghost_name}_journal.md"

    monkeypatch.setattr(ReasoningPipe, "__init__", mock_init)
    
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    pipe.log_thought("Deep thought")
    pipe.log_result("Done", {"tokens": 50})
    
    output_file = pipe.finalize()
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "# ReasoningPipe: test_agent | Session: sess_123" in content
    assert "THOUGHT: Deep thought" in content
    assert "RESULT: Done" in content
    assert "Tokens Generated**: 50" in content
    
    summary_file = journals_dir / "test_agent_journal.md"
    assert summary_file.exists()
    assert "Session: [sess_123]" in summary_file.read_text()

def test_double_finalize_warning(tmp_path, monkeypatch):
    journals_dir = tmp_path / "docs" / "journals"
    journals_dir.mkdir(parents=True)
    
    def mock_init(self, ghost_name, session_id, model, tier, agent_name=None):
        self.ghost_name = ghost_name
        self.agent_name = ghost_name  # Backward compatibility
        self.session_id = session_id
        self.model = model
        self.tier = tier
        self.start_time = datetime.now()
        self.buffer = []
        self.metrics = {"tokens": 0, "duration": 0.0, "cost": 0.0, "tokens_per_second": 0.0}
        self.task_description = None
        self.is_finalized = False
        self.journals_dir = journals_dir
        self.output_path = self.journals_dir / f"{ghost_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"{ghost_name}_journal.md"

    monkeypatch.setattr(ReasoningPipe, "__init__", mock_init)
    
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_123", model="gpt-4", tier="L1")
    pipe.finalize()
    
    # Calling finalize again should not fail and should return the same path
    path = pipe.finalize()
    assert path.exists()

def test_finalize_exception_handling(monkeypatch):
    pipe = ReasoningPipe(ghost_name="test_agent", session_id="sess_error", model="gpt-4", tier="L1")
    
    def mock_mkdir(*args, **kwargs):
        raise PermissionError("No permission")
    
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    
    with pytest.raises(ReasoningPipeWriteError):
        pipe.finalize()
