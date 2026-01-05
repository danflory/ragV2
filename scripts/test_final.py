import asyncio
import logging
import sys

# setup logging to file to see if it survives
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='test_output.log',
    filemode='w'
)

async def main():
    print("STDOUT: START")
    logging.info("LOG: START")
    try:
        from app.container import container
        print("STDOUT: CONTAINER IMPORTED")
        logging.info("LOG: CONTAINER IMPORTED")
        
        if container.memory:
            print("STDOUT: SEARCHING")
            results = await container.memory.search("roadmap")
            print(f"STDOUT: RESULTS {len(results)}")
        else:
             print("STDOUT: NO MEMORY")
             
    except Exception as e:
        print(f"STDOUT: ERROR {e}")
        logging.error(f"LOG: ERROR {e}")

if __name__ == "__main__":
    asyncio.run(main())
