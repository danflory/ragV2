import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

import asyncio

async def test():
    # Write to a file since stdout is failing us
    with open("final_ingest_log.txt", "w") as f:
        f.write("V11 START\n")
        try:
            from app.container import container
            f.write("CONTAINER LOADED\n")
            if container.ingestor:
                abs_path = os.path.abspath("docs")
                container.ingestor.docs_path = [abs_path]
                f.write(f"INGESTING: {abs_path}\n")
                summary = await container.ingestor.ingest_all()
                f.write(f"SUMMARY: {summary}\n")
                
                res = await container.memory.search("roadmap")
                f.write(f"RESULTS: {len(res)}\n")
            else:
                f.write("NO INGESTOR\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")

if __name__ == "__main__":
    asyncio.run(test())
