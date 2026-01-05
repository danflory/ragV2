import asyncio
import os
import sys

os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

async def test():
    f = open("ingest_v5_output.txt", "w")
    f.write("START\n")
    f.flush()
    try:
        from app.container import container
        f.write("CONTAINER LOADED\n")
        f.flush()
        if container.ingestor:
            f.write(f"PATH: {container.ingestor.docs_path}\n")
            f.flush()
            summary = await container.ingestor.ingest_all()
            f.write(f"SUMMARY: {summary}\n")
            f.flush()
    except Exception as e:
        f.write(f"ERROR: {e}\n")
    f.close()

if __name__ == "__main__":
    asyncio.run(test())
