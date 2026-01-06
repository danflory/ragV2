import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Mock anthropic before importing the wrapper if needed, 
# but we can just mock the instance.

from app.wrappers.claude_wrapper import ClaudeThinkingWrapper

async def test_claude_wrapper_logic():
    print("Testing ClaudeThinkingWrapper logic with mock...")
    
    # Set env var so it doesn't fail init
    os.environ["ANTHROPIC_API_KEY"] = "mock_key"
    
    wrapper = ClaudeThinkingWrapper(session_id="test_session_123")
    
    # Mock the anthropic client
    # The wrapper uses self.client = AsyncAnthropic(api_key=key)
    # We'll replace wrapper.client.messages.create
    
    # Mock events
    class MockDelta:
        def __init__(self, text):
            self.text = text
            self.type = "text_delta"
    
    class MockChunk:
        def __init__(self, type, text=None):
            self.type = type
            self.delta = MockDelta(text) if text else None
    
    chunks = [
        MockChunk("content_block_delta", "<thinking>Analyzing the theological significance of 'gravitas'...</thinking>"),
        MockChunk("content_block_delta", "Gravitas in a theological context refers to..."),
    ]
    
    # Async iterator for the response
    async def async_iter():
        for chunk in chunks:
            yield chunk
            
    wrapper.client.messages.create = AsyncMock(return_value=async_iter())
    
    task = {"prompt": "Analyze the theological significance of 'gravitas'"}
    
    # We need to make sure docs/journals exists
    os.makedirs("docs/journals", exist_ok=True)
    
    result = await wrapper.execute_task(task)
    
    print(f"Result output length: {len(result['output'])}")
    
    # Verify pipe file
    pipe_path = f"docs/journals/ReasoningPipe_Claude_Thinking_test_session_123.md"
    if os.path.exists(pipe_path):
        print(f"Pipe file created: {pipe_path}")
        with open(pipe_path, "r") as f:
            content = f.read()
            if "THOUGHT: Analyzing the theological significance" in content:
                print("✅ Found expected thought in pipe!")
            else:
                print("❌ Thought NOT found in pipe.")
                print("Content was:")
                print(content)
    else:
        print(f"❌ Pipe file NOT created at {pipe_path}")

if __name__ == "__main__":
    asyncio.run(test_claude_wrapper_logic())
