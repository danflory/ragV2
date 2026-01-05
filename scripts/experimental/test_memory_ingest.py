import asyncio
import uuid
from app.container import container

async def test():
    print("Direct memory ingest test")
    try:
        from app.container import container
        if container.memory:
            print("Memory initialized. Ingesting test chunk...")
            success = await container.memory.ingest(
                text="This is a test chunk for the Gravitas roadmap. Version is 4.2.0.",
                metadata={"source": "test_script", "type": "test"}
            )
            print(f"Ingest success: {success}")
            
            print("Searching for test chunk...")
            res = await container.memory.search("roadmap version")
            print(f"Search results: {len(res)}")
            for r in res:
                print(f"Match: {r}")
        else:
            print("Memory is None")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
