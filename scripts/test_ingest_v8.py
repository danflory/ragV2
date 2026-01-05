import asyncio
import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

# Set encoding to utf-8 just in case
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    # Write to file directly
    with open("ingest_v8_output.txt", "w") as f:
        f.write("Ingest test v8 start\n")
        from app.container import container
        
        if container.ingestor:
            abs_docs = os.path.abspath("docs")
            container.ingestor.docs_path = [abs_docs]
            f.write(f"Path: {container.ingestor.docs_path}\n")
            
            summary = await container.ingestor.ingest_all()
            f.write(f"Summary: {summary}\n")
            
            res = await container.memory.search("roadmap")
            f.write(f"Results: {len(res)}\n")
            if res:
                f.write(f"Match: {res[0][:300]}\n")
        else:
            f.write("No ingestor\n")

if __name__ == "__main__":
    asyncio.run(test())
