import pytest
import respx
from httpx import Response
from app.clients.deepinfra import DeepInfraClient
from app.clients.gemini import GeminiClient

@pytest.mark.asyncio
async def test_deepinfra_client_mock():
    client = DeepInfraClient(api_key="test_key")
    
    with respx.mock:
        respx.post("https://api.deepinfra.com/v1/openai/chat/completions").mock(
            return_value=Response(200, json={"choices": [{"message": {"content": "Hello from DeepInfra"}}]})
        )
        
        response = await client.chat_completion("some-model", [{"role": "user", "content": "Hi"}])
        assert response["choices"][0]["message"]["content"] == "Hello from DeepInfra"

@pytest.mark.asyncio
async def test_gemini_client_mock():
    client = GeminiClient(api_key="test_key")
    
    with respx.mock:
        # Match the URL pattern including the API key
        respx.post(url__regex=r"https://generativelanguage\.googleapis\.com/.*").mock(
            return_value=Response(200, json={"candidates": [{"content": {"parts": [{"text": "Hello from Gemini"}]}}]})
        )
        
        response = await client.generate_content("gemini-1.5-flash", [{"parts": [{"text": "Hi"}]}])
        assert response["candidates"][0]["content"]["parts"][0]["text"] == "Hello from Gemini"
