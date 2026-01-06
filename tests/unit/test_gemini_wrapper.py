import pytest
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from unittest.mock import MagicMock, AsyncMock
from app.wrappers.gemini_wrapper import GeminiWrapper
from app.services.supervisor.guardian import SupervisorGuardian
from app.lib.reasoning_pipe import ReasoningPipe

@pytest.fixture
def mock_certs_dir(tmp_path):
    d = tmp_path / "certs"
    d.mkdir()
    cert_data = {
        "agent_name": "Gemini_Thinking",
        "issued_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "signature": "mock",
        "version": "1.0"
    }
    (d / "Gemini_Thinking.json").write_text(json.dumps(cert_data))
    return d

@pytest.fixture
def mock_journals_dir(tmp_path):
    d = tmp_path / "journals"
    d.mkdir()
    return d

@pytest.mark.asyncio
async def test_gemini_wrapper_execute(mock_certs_dir, mock_journals_dir, monkeypatch):
    # Set environment variable for API key
    monkeypatch.setenv("GOOGLE_API_KEY", "mock_key")
    
    # Mock SupervisorGuardian to use our temp certs dir
    original_guardian_init = SupervisorGuardian.__init__
    def mock_guardian_init(self, certificates_dir=str(mock_certs_dir)):
        original_guardian_init(self, certificates_dir=certificates_dir)
    monkeypatch.setattr(SupervisorGuardian, "__init__", mock_guardian_init)

    # Mock ReasoningPipe to use our temp journals dir
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
        self.journals_dir = mock_journals_dir
        self.output_path = self.journals_dir / f"ReasoningPipe_{agent_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"ReasoningPipe_{agent_name}.md"
    monkeypatch.setattr(ReasoningPipe, "__init__", mock_pipe_init)

    # Mock Gemini Client
    mock_model_instance = MagicMock()
    
    # Create a mock async stream response
    class MockChunk:
        def __init__(self, text=None, thinking=None):
            self.text = text
            self.thinking = thinking
            self.candidates = []

    class MockAsyncResponse:
        def __init__(self, chunks):
            self.chunks = chunks
        def __aiter__(self):
            return self
        async def __anext__(self):
            if not self.chunks:
                raise StopAsyncIteration
            return self.chunks.pop(0)

    mock_response = MockAsyncResponse([
        MockChunk(thinking="Let's think about this."),
        MockChunk(text="The answer is 42.")
    ])
    
    mock_model_instance.generate_content_async = AsyncMock(return_value=mock_response)
    
    # Patch genai.GenerativeModel to return our mock instance
    import google.generativeai as genai
    monkeypatch.setattr(genai, "GenerativeModel", lambda model_name: mock_model_instance)
    monkeypatch.setattr(genai, "configure", lambda api_key: None)

    wrapper = GeminiWrapper(session_id="gemini_sess_001")
    result = await wrapper.execute_task({"prompt": "What is the meaning of life?"})
    
    assert "The answer is 42" in result["output"]
    
    # Check if ReasoningPipe was written
    pipe_file = mock_journals_dir / "ReasoningPipe_Gemini_Thinking_gemini_sess_001.md"
    assert pipe_file.exists()
    
    content = pipe_file.read_text()
    assert "THOUGHT: Let's think about this." in content
    assert "RESULT: Generated 17 characters." in content
