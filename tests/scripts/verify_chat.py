import asyncio
import sys
import os

# Fix path so we can import 'app'
sys.path.insert(0, os.getcwd())

from app.router import chat_endpoint, ChatRequest

async def main():
    print("🐢 Sending prompt to Local L1 (Titan RTX)...")
    
    # 1. Create the request object (simulating a legitimate API call)
    req = ChatRequest(message="Write a haiku about Python code.")
    
    # 2. Call the endpoint directly
    result = await chat_endpoint(req)
    
    # 3. Print the result
    print("\n🤖 L1 Response:")
    print(f"--------------------------------------------------")
    print(result["response"])
    print(f"--------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
    