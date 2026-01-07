
import pytest
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from unittest.mock import MagicMock, AsyncMock
from app.wrappers.claude_wrapper import ClaudeThinkingWrapper
from app.services.supervisor.guardian import SupervisorGuardian
from app.lib.reasoning_pipe import ReasoningPipe

@pytest.fixture
def mock_certs_dir(tmp_path):
    d = tmp_path / "certs"
    d.mkdir()
    cert_data = {
        "agent_name": "Claude_Thinking",
        "issued_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "signature": "mock",
        "version": "1.0"
    }
    (d / "Claude_Thinking.json").write_text(json.dumps(cert_data))
    return d

@pytest.fixture
def mock_journals_dir(tmp_path):
    d = tmp_path / "journals"
    d.mkdir()
    return d

@pytest.mark.asyncio
async def test_claude_wrapper_execute(mock_certs_dir, mock_journals_dir, monkeypatch):
    # Set environment variable for API key
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock_key")
    
    # Mock SupervisorGuardian to use our temp certs dir
    original_guardian_init = SupervisorGuardian.__init__
    def mock_guardian_init(self, certificates_dir=str(mock_certs_dir)):
        original_guardian_init(self, certificates_dir=certificates_dir)
    monkeypatch.setattr(SupervisorGuardian, "__init__", mock_guardian_init)

    # Mock ReasoningPipe to use our temp journals dir
    def mock_pipe_init(self, ghost_name, session_id, model, tier, agent_name=None):
        self.ghost_name = ghost_name
        self.agent_name = ghost_name
        self.session_id = session_id
        self.model = model
        self.tier = tier
        self.start_time = datetime.now()
        self.buffer = []
        self.metrics = {"tokens": 0, "duration": 0.0, "cost": 0.0, "tokens_per_second": 0.0}
        self.task_description = None
        self.is_finalized = False
        self.journals_dir = mock_journals_dir
        self.output_path = self.journals_dir / f"{ghost_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"{ghost_name}_journal.md"
    monkeypatch.setattr(ReasoningPipe, "__init__", mock_pipe_init)

    # Mock Anthropic Client
    mock_client_instance = AsyncMock()
    
    # Create a mock async stream response
    class MockChunk:
        def __init__(self, type, delta=None):
            self.type = type
            self.delta = delta

    class MockDelta:
        def __init__(self, text):
            self.text = text

    class MockAsyncResponse:
        def __init__(self, chunks):
            self.chunks = chunks
        def __aiter__(self):
            return self
        async def __anext__(self):
            if not self.chunks:
                raise StopAsyncIteration
            return self.chunks.pop(0)

    # Mock chunks mimicking Anthropic response
    chunks = [
        MockChunk(type="content_block_delta", delta=MockDelta("<thinking>Thinking deeply...</thinking>")),
        MockChunk(type="content_block_delta", delta=MockDelta("The answer is 42."))
    ]
    mock_response = MockAsyncResponse(chunks)
    
    # Setup the mock message create call
    mock_client_instance.messages.create.return_value = mock_response

    # Patch AsyncAnthropic where it is used
    monkeypatch.setattr("app.wrappers.claude_wrapper.AsyncAnthropic", lambda api_key: mock_client_instance)

    wrapper = ClaudeThinkingWrapper(session_id="claude_sess_001")
    result = await wrapper.execute_task({"prompt": "What is 6 * 7?"})
    
    assert "The answer is 42." in result["output"]
    
    # Check if ReasoningPipe was written
    pipe_file = mock_journals_dir / "Claude_Thinking_claude_sess_001.md"
    assert pipe_file.exists()
    
    content = pipe_file.read_text()
    assert "THOUGHT: Thinking deeply..." in content
    assert "RESULT: Generated" in content
    assert "characters." in content
