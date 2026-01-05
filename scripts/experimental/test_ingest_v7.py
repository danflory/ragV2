import asyncio
import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    # setup logging
    import logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    print("Ingest test v7 start", flush=True)
    from app.container import container
    if container.ingestor:
        abs_docs = os.path.abspath("docs")
        container.ingestor.docs_path = [abs_docs]
        print(f"Path: {container.ingestor.docs_path}")
        summary = await container.ingestor.ingest_all()
        print(f"Summary: {summary}")
        res = await container.memory.search("roadmap")
        print(f"Results: {len(res)}")
    else:
        print("No ingestor")

if __name__ == "__main__":
    asyncio.run(test())
