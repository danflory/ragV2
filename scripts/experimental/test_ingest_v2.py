import asyncio
import logging
import sys

logging.basicConfig(level=logging.INFO)

async def test():
    print("Ingest test v2 start", flush=True)
    try:
        from app.container import container
        print("Container loaded", flush=True)
        if container.ingestor:
            print("Running ingestion...", flush=True)
            summary = await container.ingestor.ingest_all()
            print(f"Summary: {summary}", flush=True)
        else:
            print("No ingestor", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
