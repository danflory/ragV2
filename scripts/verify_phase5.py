import httpx
import asyncio
import json

async def test_routing():
    url = "http://localhost:8000/v1/chat/completions"
    
    print("Test 1: Normal Complexity (Should go to L1)")
    payload_l1 = {
        "model": "gemma2",
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "complexity": 2
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload_l1, timeout=10.0)
            print(f"L1 Response Status: {resp.status_code}")
            print(f"L1 Response: {resp.text[:100]}...")
    except Exception as e:
        print(f"L1 Request failed (Expected if Ollama is not responding): {e}")

    print("\nTest 2: High Complexity (Should go to L3/Gemini)")
    payload_l3 = {
        "model": "gemma2",
        "messages": [{"role": "user", "content": "Analyze this repo architecture."}],
        "complexity": 10
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload_l3, timeout=10.0)
            print(f"L3 Response Status: {resp.status_code}")
            # This should be a 500 or error json because keys are missing
            print(f"L3 Response Content: {resp.text}")
    except Exception as e:
        print(f"L3 Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_routing())
