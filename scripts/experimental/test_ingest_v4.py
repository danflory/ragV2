import asyncio
import os
import sys

# Force output
sys.stdout.reconfigure(line_buffering=True)

os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    print("Ingest test v4 start", flush=True)
    try:
        from app.container import container
        print("Container initialized", flush=True)
        if container.ingestor:
            print(f"Ingestor path: {container.ingestor.docs_path}", flush=True)
            print("Purging memory...", flush=True)
            await container.memory.purge()
            print("Running ingestion...", flush=True)
            summary = await container.ingestor.ingest_all()
            print(f"Summary: {summary}", flush=True)
        else:
            print("No ingestor", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
