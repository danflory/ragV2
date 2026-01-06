import asyncio
import os
import sys
from app.clients.deepinfra import DeepInfraClient
from app.clients.gemini import GeminiClient

async def main():
    print("--- Testing Connection: DeepInfra ---")
    deepinfra_key = os.getenv("DEEPINFRA_API_KEY") or os.getenv("L2_KEY")
    if not deepinfra_key:
        print("SKIP: DEEPINFRA_API_KEY or L2_KEY not found in environment.")
    else:
        client = DeepInfraClient(api_key=deepinfra_key)
        success = await client.test_connection()
        print(f"DeepInfra Connection: {'SUCCESS' if success else 'FAILED'}")

    print("\n--- Testing Connection: Gemini ---")
    gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("L3_KEY")
    if not gemini_key:
        print("SKIP: GOOGLE_API_KEY or L3_KEY not found in environment.")
    else:
        client = GeminiClient(api_key=gemini_key)
        success = await client.test_connection()
        print(f"Gemini Connection: {'SUCCESS' if success else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())
