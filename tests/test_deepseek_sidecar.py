import requests
import json
import pytest

def test_deepseek_sidecar_connection():
    """Test the DeepSeek Coder v2 model via OpenAI-compatible endpoint"""
    
    # Test endpoint
    url = "http://localhost:11434/v1/chat/completions"
    
    # Test payload
    payload = {
        "model": "deepseek-coder-v2:16b",
        "messages": [
            {
                "role": "user", 
                "content": "Print hello world in python"
            }
        ]
    }
    
    # Send request
    response = requests.post(url, json=payload)
    
    # Assertions
    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    
    response_data = response.json()
    assert "choices" in response_data, "Response should contain 'choices' field"
    assert len(response_data["choices"]) > 0, "Response should have at least one choice"
    assert "message" in response_data["choices"][0], "Choice should contain 'message' field"
    assert "content" in response_data["choices"][0]["message"], "Message should contain 'content' field"
    assert response_data["choices"][0]["message"]["content"], "Content should not be empty"
    
    print("✅ DeepSeek Sidecar test passed!")
    print(f"Response: {response_data['choices'][0]['message']['content']}")

if __name__ == "__main__":
    test_deepseek_sidecar_connection()
