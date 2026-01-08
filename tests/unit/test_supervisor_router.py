import os
import pytest
from app.services.supervisor.router import SupervisorEngine
from app.services.registry.shell_registry import ModelTier, ShellRegistry
from app.wrappers.ollama_wrapper import OllamaWrapper
from app.wrappers.gemini_wrapper import GeminiWrapper
from app.wrappers.claude_wrapper import ClaudeThinkingWrapper
from app.wrappers.deepinfra_wrapper import DeepInfraWrapper

def test_ollama_url_parsing():
    engine = SupervisorEngine()
    
    # Test case 1: Standard URL
    os.environ["OLLAMA_URL"] = "http://localhost:11434"
    wrapper = engine.get_wrapper("test_ghost", "gemma2:27b", ModelTier.L1, "session_123")
    assert isinstance(wrapper, OllamaWrapper)
    assert wrapper.ollama_url == "http://localhost:11434"
    
    # Test case 2: URL with trailing V1 path
    os.environ["OLLAMA_URL"] = "http://ollama-server:11434/v1/chat/completions"
    wrapper = engine.get_wrapper("test_ghost", "gemma2:27b", ModelTier.L1, "session_123")
    assert wrapper.ollama_url == "http://ollama-server:11434"
    
    # Test case 3: URL with v1 in the domain name (edge case)
    os.environ["OLLAMA_URL"] = "http://v1-instance.internal:11434"
    wrapper = engine.get_wrapper("test_ghost", "gemma2:27b", ModelTier.L1, "session_123")
    assert wrapper.ollama_url == "http://v1-instance.internal:11434"

def test_provider_based_routing():
    engine = SupervisorEngine()
    
    # Test Ollama (L1)
    wrapper = engine.get_wrapper("test_ghost", "gemma2:27b", ModelTier.L1, "session_123")
    assert isinstance(wrapper, OllamaWrapper)
    
    # Test Gemini (L3)
    wrapper = engine.get_wrapper("test_ghost", "gemini-1.5-pro", ModelTier.L3, "session_123")
    assert isinstance(wrapper, GeminiWrapper)
    
    # Test Claude (L3)
    wrapper = engine.get_wrapper("test_ghost", "claude-3-5-sonnet", ModelTier.L3, "session_123")
    assert isinstance(wrapper, ClaudeThinkingWrapper)
    
    # Test DeepInfra (L2)
    wrapper = engine.get_wrapper("test_ghost", "meta-llama/Meta-Llama-3-70B-Instruct", ModelTier.L2, "session_123")
    assert isinstance(wrapper, DeepInfraWrapper)

def test_fallback_routing():
    engine = SupervisorEngine()
    
    # Test unregistered model with tier mapping
    # Assuming "unknown-model" is not in registry
    wrapper = engine.get_wrapper("test_ghost", "unknown-model", ModelTier.L1, "session_123")
    assert isinstance(wrapper, OllamaWrapper)
    
    wrapper = engine.get_wrapper("test_ghost", "some-gemini-custom", ModelTier.L3, "session_123")
    assert isinstance(wrapper, GeminiWrapper)
