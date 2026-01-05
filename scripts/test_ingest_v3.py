import asyncio
import os

os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    print("Ingest test v3 start")
    from app.container import container
    if container.ingestor:
        print("Running ingestion...")
        summary = await container.ingestor.ingest_all()
        print(f"Summary: {summary}")
    else:
        print("No ingestor")

if __name__ == "__main__":
    asyncio.run(test())
