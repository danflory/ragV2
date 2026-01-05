import httpx
import asyncio

async def test():
    url = "http://localhost:11434/api/tags"
    print(f"Connecting to {url}...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            print(f"Data: {resp.json()}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
