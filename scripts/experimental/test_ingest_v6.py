import asyncio
import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    print("Ingest test v6 start", flush=True)
    try:
        from app.container import container
        print("Container initialized", flush=True)
        if container.ingestor:
            # Override DOCS_PATH here to be absolute
            abs_docs = os.path.abspath("docs")
            container.ingestor.docs_path = [abs_docs]
            print(f"Overridden path: {container.ingestor.docs_path}", flush=True)
            
            print("Purging...", flush=True)
            await container.memory.purge()
            
            print("Ingesting all...", flush=True)
            summary = await container.ingestor.ingest_all()
            print(f"Summary: {summary}", flush=True)
            
            print("Searching for roadmap...", flush=True)
            res = await container.memory.search("roadmap")
            print(f"Search results: {len(res)}", flush=True)
            if res:
                print(f"First result head: {res[0][:200]}", flush=True)
        else:
            print("No ingestor")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
