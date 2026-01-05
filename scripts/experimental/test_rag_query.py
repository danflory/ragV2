#!/usr/bin/env python3
"""
Test RAG query through the Docker API
"""
import httpx
import asyncio
import json

async def test_rag():
    print("=" * 80)
    print("TESTING RAG QUERY")
    print("=" * 80)
    
    url = "http://localhost:5050/chat"
    payload = {"message": "Summarize the roadmap for Gravitas"}
    
    print(f"\nSending request to {url}")
    print(f"Query: {payload['message']}\n")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Response received:")
                print("-" * 80)
                print(f"Layer: {data.get('layer', 'unknown')}")
                print(f"\nResponse:\n{data.get('response', 'No response')}")
                print("-" * 80)
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag())
