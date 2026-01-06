import pytest
import asyncio
import os
import json
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

from app.services.supervisor.certifier import WrapperCertifier
from app.services.supervisor.guardian import SupervisorGuardian

# --- Fixtures ---

@pytest.fixture
def certifier(tmp_path):
    certs_dir = tmp_path / "certs"
    certs_dir.mkdir()
    Path("docs/journals").mkdir(parents=True, exist_ok=True)
    return WrapperCertifier(certificates_dir=str(certs_dir))

# Mock Response for Gemini
class MockGeminiChunk:
    def __init__(self, text, thinking=None):
        self.text = text
        self.thinking = thinking
        self.candidates = [MagicMock()]
        self.candidates[0].content.parts = [MagicMock()]
        self.candidates[0].content.parts[0].text = thinking if thinking else text
        self.candidates[0].content.parts[0].thought = True if thinking else False

# Mock Response for Claude
class MockClaudeChunk:
    def __init__(self, text=None, type="content_block_delta"):
        self.type = type
        self.delta = MagicMock()
        self.delta.text = text

# Mock Response for DeepInfra (OpenAI-like)
class MockOpenAIChunk:
    def __init__(self, content):
        delta = MagicMock()
        delta.content = content
        choice = MagicMock()
        choice.delta = delta
        self.choices = [choice]

# --- Tests ---

class TestGeminiWrapperCertification:
    @pytest.mark.asyncio
    async def test_gemini_wrapper_certifies_successfully(self, certifier):
        wrapper_path = "app/wrappers/gemini_wrapper.py"
        
        mock_model = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockGeminiChunk("The word 'gravitas' means weight or seriousness.", thinking="Thinking about the definition of gravitas...")
        ]
        mock_model.generate_content_async = AsyncMock(return_value=mock_response)
        
        with patch("google.generativeai.GenerativeModel", return_value=mock_model), \
             patch("google.generativeai.configure"), \
             patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "Gemini_Agent")
            assert result.passed is True

    @pytest.mark.asyncio
    async def test_gemini_wrapper_produces_valid_pipe(self, certifier):
        wrapper_path = "app/wrappers/gemini_wrapper.py"
        mock_model = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockGeminiChunk("Response text", thinking="Some thought")
        ]
        mock_model.generate_content_async = AsyncMock(return_value=mock_response)
        
        with patch("google.generativeai.GenerativeModel", return_value=mock_model), \
             patch("google.generativeai.configure"), \
             patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "Gemini_Agent")
            assert result.validation.passed is True
            content = result.test.pipe_file.read_text()
            assert "THOUGHT: Some thought" in content

    @pytest.mark.asyncio
    async def test_gemini_wrapper_handles_api_errors(self, certifier):
        wrapper_path = "app/wrappers/gemini_wrapper.py"
        mock_model = MagicMock()
        mock_model.generate_content_async = AsyncMock(side_effect=Exception("API Runtime Error"))
        
        with patch("google.generativeai.GenerativeModel", return_value=mock_model), \
             patch("google.generativeai.configure"), \
             patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "Gemini_Agent")
            assert result.passed is False
            assert "API Runtime Error" in result.test.error

class TestClaudeWrapperCertification:
    @pytest.mark.asyncio
    async def test_claude_wrapper_certifies_successfully(self, certifier):
        wrapper_path = "app/wrappers/claude_wrapper.py"
        
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockClaudeChunk("<thinking>Searching for gravitas definition...</thinking>"),
            MockClaudeChunk("Gravitas refers to dignity or importance.")
        ]
        mock_messages.create = AsyncMock(return_value=mock_response)
        mock_client.messages = mock_messages
        
        with patch("anthropic.AsyncAnthropic", return_value=mock_client), \
             patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "Claude_Thinking")
            assert result.passed is True

    @pytest.mark.asyncio
    async def test_claude_wrapper_parses_thinking_tags(self, certifier):
        wrapper_path = "app/wrappers/claude_wrapper.py"
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockClaudeChunk("<thinking>Core thought</thinking>"),
            MockClaudeChunk("Result text")
        ]
        mock_messages.create = AsyncMock(return_value=mock_response)
        mock_client.messages = mock_messages
        
        with patch("anthropic.AsyncAnthropic", return_value=mock_client), \
             patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "Claude_Thinking")
            assert result.passed is True
            content = result.test.pipe_file.read_text()
            assert "THOUGHT: Core thought" in content

class TestOllamaWrapperCertification:
    @pytest.mark.asyncio
    async def test_ollama_wrapper_certifies_successfully(self, certifier):
        wrapper_path = "app/wrappers/ollama_wrapper.py"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        async def async_lines():
            yield json.dumps({"response": "<think>Processing...</think>gravitas means weight.", "done": True})
        
        mock_response.aiter_lines = lambda: async_lines()
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_client = MagicMock()
        mock_client.stream = MagicMock(return_value=mock_context)
        mock_client.__aenter__.return_value = mock_client
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await certifier.certify_wrapper(wrapper_path, "Ollama_Agent")
            assert result.passed is True

    @pytest.mark.asyncio
    async def test_ollama_wrapper_supports_multiple_models(self, certifier):
        wrapper_path = "app/wrappers/ollama_wrapper.py"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        async def async_lines():
            yield json.dumps({"response": "<think>Thinking...</think>Done.", "done": True})
            
        mock_response.aiter_lines = lambda: async_lines()
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_client = MagicMock()
        mock_client.stream = MagicMock(return_value=mock_context)
        mock_client.__aenter__.return_value = mock_client
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            result1 = await certifier.certify_wrapper(wrapper_path, "Ollama_Llama3")
            result2 = await certifier.certify_wrapper(wrapper_path, "Ollama_Mistral")
            
            assert result1.passed is True
            assert result2.passed is True

class TestDeepInfraWrapperCertification:
    @pytest.mark.asyncio
    async def test_deepinfra_wrapper_certifies_successfully(self, certifier):
        wrapper_path = "app/wrappers/deepinfra_wrapper.py"
        
        mock_client = MagicMock()
        mock_completions = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockOpenAIChunk("Definition of gravitas"),
            MockOpenAIChunk(" and its history.")
        ]
        mock_completions.create = AsyncMock(return_value=mock_response)
        mock_client.chat = MagicMock()
        mock_client.chat.completions = mock_completions
        
        with patch("openai.AsyncOpenAI", return_value=mock_client), \
             patch.dict(os.environ, {"DEEPINFRA_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "DeepInfra_Agent")
            assert result.passed is True

    @pytest.mark.asyncio
    async def test_deepinfra_wrapper_produces_valid_pipe(self, certifier):
        wrapper_path = "app/wrappers/deepinfra_wrapper.py"
        mock_client = MagicMock()
        mock_completions = MagicMock()
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockOpenAIChunk("Chunk 1"),
            MockOpenAIChunk("Chunk 2")
        ]
        mock_completions.create = AsyncMock(return_value=mock_response)
        mock_client.chat = MagicMock()
        mock_client.chat.completions = mock_completions
        
        with patch("openai.AsyncOpenAI", return_value=mock_client), \
             patch.dict(os.environ, {"DEEPINFRA_API_KEY": "fake-key"}):
            result = await certifier.certify_wrapper(wrapper_path, "DeepInfra_Agent")
            assert result.passed is True
            content = result.test.pipe_file.read_text()
            assert "THOUGHT: Processing: Chunk 1..." in content
