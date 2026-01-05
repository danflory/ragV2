import os
import sys

# Metal overrides
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

import asyncio

async def test():
    with open("v12_log.txt", "w") as f:
        f.write("V12 START\n")
        try:
            from app.container import container
            f.write("CONTAINER LOADED\n")
            if container.ingestor:
                abs_docs = os.path.abspath("docs")
                container.ingestor.docs_path = [abs_docs]
                
                # Manual Ingest walk
                f.write(f"Scout walking {abs_docs}\n")
                files = os.listdir(abs_docs)
                f.write(f"Files: {files}\n")
                
                # Just ingest ROADMAP.md directly for proof
                roadmap_path = os.path.join(abs_docs, "ROADMAP.md")
                if os.path.exists(roadmap_path):
                    f.write("Found ROADMAP.md\n")
                    with open(roadmap_path, "r") as r:
                         content = r.read()
                    f.write(f"Read {len(content)} chars\n")
                    
                    success = await container.memory.ingest(
                         text=content,
                         metadata={"source": "ROADMAP.md", "type": "manual_test"}
                    )
                    f.write(f"Ingest success: {success}\n")
                    
                    # Search
                    res = await container.memory.search("roadmap infrastructure")
                    f.write(f"Results: {len(res)}\n")
                    if res:
                        f.write(f"Content: {res[0][:200]}\n")
                else:
                    f.write("ROADMAP.md not found\n")
            else:
                f.write("NO INGESTOR\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")

if __name__ == "__main__":
    asyncio.run(test())
