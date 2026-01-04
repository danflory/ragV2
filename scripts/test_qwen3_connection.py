#!/usr/bin/env python3
"""
Independent Qwen3 Connection Test Script
No external dependencies - uses only httpx for HTTP requests
"""

import asyncio
import httpx
import json

# === CONFIGURATION (Replace with your actual values) ===
DEEPINFRA_API_KEY = "aeuujtsMyv1WoT7oRAsOzH6UUS7BCV0u"
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
QWEN3_MODEL = "Qwen/Qwen3-Coder-480B-A35B-Instruct"

async def test_qwen3_connection():
    """Test connection to Qwen3 model on DeepInfra"""
    print(f"🔌 Testing Qwen3 Connection")
    print(f"   Model: {QWEN3_MODEL}")
    print(f"   URL: {DEEPINFRA_URL}")
    print(f"   API Key: {'✅ Set' if DEEPINFRA_API_KEY else '❌ Missing'}")

    if not DEEPINFRA_API_KEY:
        print("❌ Cannot proceed without API key")
        return False

    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": QWEN3_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("📨 Sending test request...")
            response = await client.post(DEEPINFRA_URL, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS! Connection working")
                print(f"Response: {data['choices'][0]['message']['content']}")
                return True
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_qwen3_connection())
    exit(0 if success else 1)
