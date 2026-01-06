import asyncio
import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.wrappers.ollama_wrapper import OllamaWrapper

# Async iterator for the response stream
class MockStreamResponse:
    def __init__(self, chunks):
        self.chunks = chunks
        self.status_code = 200
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
        
    async def aiter_lines(self):
        for chunk in self.chunks:
            yield json.dumps(chunk)

class MockAsyncClient:
    def __init__(self, chunks, **kwargs):
        self.chunks = chunks
    
    def stream(self, method, url, **kwargs):
        return MockStreamResponse(self.chunks)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

async def test_ollama_wrapper_logic():
    print("Testing OllamaWrapper logic with custom mock class...")
    
    wrapper = OllamaWrapper(session_id="test_ollama_456", model_name="codellama:7b")
    
    # Mock events
    chunks = [
        {"model": "codellama:7b", "response": "<think>Wait, I should use a simple loop.</think>", "done": False},
        {"model": "codellama:7b", "response": "Here is a factorial function:", "done": False},
        {"model": "codellama:7b", "response": "\n```python\ndef factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\n```", "done": True, "eval_count": 42}
    ]
    
    # Patch httpx.AsyncClient
    import httpx
    original_client = httpx.AsyncClient
    httpx.AsyncClient = lambda **kwargs: MockAsyncClient(chunks, **kwargs)
    
    task = {"prompt": "Write a Python function to calculate factorial"}
    
    # Ensure docs/journals exists
    os.makedirs("docs/journals", exist_ok=True)
    
    try:
        result = await wrapper.execute_task(task)
        print(f"Result output length: {len(result['output'])}")
        
        # Verify pipe file
        pipe_path = f"docs/journals/ReasoningPipe_Ollama_codellama_7b_test_ollama_456.md"
        if os.path.exists(pipe_path):
            print(f"Pipe file created: {pipe_path}")
            with open(pipe_path, "r") as f:
                content = f.read()
                if "THOUGHT: Wait, I should use a simple loop." in content:
                    print("✅ Found expected thought in pipe!")
                else:
                    print("❌ Thought NOT found in pipe.")
                
                if "Tokens Generated**: 42" in content:
                    print("✅ Correct token count captured!")
                else:
                    print("❌ Token count MISMATCH.")
        else:
            print(f"❌ Pipe file NOT created at {pipe_path}")
            
    finally:
        # Restore httpx.AsyncClient
        httpx.AsyncClient = original_client

if __name__ == "__main__":
    asyncio.run(test_ollama_wrapper_logic())
