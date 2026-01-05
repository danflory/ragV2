import asyncio
import logging
import sys
import os

# SET METAL OVERRIDES
os.environ["QDRANT_HOST"] = "localhost"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["DB_HOST"] = "localhost"
os.environ["L1_URL"] = "http://localhost:11434"

# setup logging to file to see if it survives
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='test_output_metal.log',
    filemode='w'
)

async def main():
    print("STDOUT: START", flush=True)
    logging.info("LOG: START")
    try:
        from app.container import container
        print("STDOUT: CONTAINER IMPORTED", flush=True)
        logging.info("LOG: CONTAINER IMPORTED")
        
        if container.memory:
            print("STDOUT: SEARCHING", flush=True)
            results = await container.memory.search("roadmap")
            print(f"STDOUT: RESULTS {len(results)}", flush=True)
            for r in results:
                print(f"MATCH: {r[:100]}", flush=True)
        else:
             print("STDOUT: NO MEMORY", flush=True)
             
    except Exception as e:
        print(f"STDOUT: ERROR {e}", flush=True)
        logging.error(f"LOG: ERROR {e}")

if __name__ == "__main__":
    asyncio.run(main())
