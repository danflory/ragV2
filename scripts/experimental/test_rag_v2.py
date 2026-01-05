import asyncio
import logging
import sys

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)

async def test():
    print("🚀 Starting test_rag_v2.py")
    try:
        from app.container import container
        print("✅ Container imported")
        
        if not container.memory:
            print("❌ Container memory is None. Checking initialization...")
            # The container should have logged why it failed.
            return

        query = "roadmap"
        print(f"🔎 Searching for: {query}")
        results = await container.memory.search(query, top_k=5)
        print(f"✅ Found {len(results)} results")
        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} ---\n{res[:300]}...")
            
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
