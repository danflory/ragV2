import asyncio
from app.container import container
from app.config import config

async def test():
    print("🔌 Connecting to services...")
    # Initialize necessary components
    from app.database import db
    # Mock some things if needed or just try a search
    # Note: container init happens on import
    
    query = "roadmap"
    print(f"🔎 Searching for: {query}")
    if container.memory:
        try:
            results = await container.memory.search(query, top_k=5)
            print(f"✅ Found {len(results)} results")
            for i, res in enumerate(results):
                print(f"--- Result {i+1} ---")
                print(res[:200] + "...")
        except Exception as e:
            print(f"❌ Search failed: {e}")
    else:
        print("❌ Memory not initialized in container")

if __name__ == "__main__":
    asyncio.run(test())
