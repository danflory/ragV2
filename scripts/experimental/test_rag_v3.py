import asyncio
import os
import sys

# Set encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("Test v3 start", flush=True)
    try:
        from app.container import container
        print("Container loaded", flush=True)
        if container.memory:
            print("Memory found, searching...", flush=True)
            results = await container.memory.search("roadmap", top_k=5)
            print(f"Results: {len(results)}", flush=True)
            for r in results:
                print("---", flush=True)
                print(r[:200], flush=True)
        else:
            print("Memory is None", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
