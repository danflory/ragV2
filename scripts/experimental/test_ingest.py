import asyncio
import os
from app.container import container

async def test():
    print("Ingest test start")
    if container.ingestor:
        print("Running ingestion...")
        summary = await container.ingestor.ingest_all()
        print(f"Summary: {summary}")
    else:
        print("No ingestor")

if __name__ == "__main__":
    asyncio.run(test())
