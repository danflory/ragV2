import asyncio
import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    print("V9 START")
    try:
        from app.container import container
        print("CONTAINER INIT")
        if container.ingestor:
             abs_path = os.path.abspath("docs")
             container.ingestor.docs_path = [abs_path]
             print(f"INGESTING: {abs_path}")
             summary = await container.ingestor.ingest_all()
             print(f"SUMMARY: {summary}")
             
             print("SEARCHING...")
             res = await container.memory.search("roadmap")
             print(f"RESULTS: {len(res)}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test())
