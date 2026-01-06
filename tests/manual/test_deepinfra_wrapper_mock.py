import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.wrappers.deepinfra_wrapper import DeepInfraWrapper

async def test_deepinfra_wrapper_logic():
    print("Testing DeepInfraWrapper logic with mock...")
    
    # Set env var
    os.environ["DEEPINFRA_API_KEY"] = "mock_key"
    
    wrapper = DeepInfraWrapper(session_id="test_deepinfra_789")
    
    # Mock the openai client response
    class MockDelta:
        def __init__(self, content):
            self.content = content

    class MockChoice:
        def __init__(self, content):
            self.delta = MockDelta(content)

    class MockChunk:
        def __init__(self, content):
            self.choices = [MockChoice(content)]
    
    chunks = [
        MockChunk("async def"),
        MockChunk(" factorial(n):"),
        MockChunk("\n    pass")
    ]
    
    # Async iterator
    async def async_iter():
        for chunk in chunks:
            yield chunk
            
    wrapper.client.chat.completions.create = AsyncMock(return_value=async_iter())
    
    task = {"prompt": "Refactor this code to use async/await: [simple sync code]"}
    
    # Ensure docs/journals exists
    os.makedirs("docs/journals", exist_ok=True)
    
    result = await wrapper.execute_task(task)
    
    print(f"Result output: {result['output']}")
    
    # Verify pipe file
    pipe_path = f"docs/journals/ReasoningPipe_DeepInfra_Qwen2.5-Coder_test_deepinfra_789.md"
    if os.path.exists(pipe_path):
        print(f"Pipe file created: {pipe_path}")
        with open(pipe_path, "r") as f:
            content = f.read()
            if "THOUGHT: Processing: async def..." in content:
                print("✅ Found expected placeholder thought in pipe!")
            else:
                print("❌ Thought NOT found in pipe.")
                print("Content was:")
                print(content)
    else:
        print(f"❌ Pipe file NOT created at {pipe_path}")

if __name__ == "__main__":
    asyncio.run(test_deepinfra_wrapper_logic())
