import asyncio
from app.database import db

async def test():
    print("Connecting to DB...")
    await db.connect()
    if db.pool:
        print("Connected!")
        async with db.pool.acquire() as conn:
            res = await conn.fetchval("SELECT 1")
            print(f"Fetchval: {res}")
    else:
        print("No pool")

if __name__ == "__main__":
    asyncio.run(test())
