import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import db

async def show_stats():
    await db.connect()
    if not db.is_ready():
        print("❌ Could not connect to database.")
        return

    async with db.pool.acquire() as conn:
        # 1. Total Token Usage
        totals = await conn.fetchrow('''
            SELECT 
                COUNT(*) as total_requests,
                SUM(prompt_tokens) as total_prompt,
                SUM(completion_tokens) as total_completion
            FROM usage_stats
        ''')

        print("\n📊 --- GRAVITAS USAGE STATS ---")
        print(f"Total Requests: {totals['total_requests'] or 0}")
        print(f"Total Tokens:   {(totals['total_prompt'] or 0) + (totals['total_completion'] or 0):,}")
        print(f"  └─ Prompt:     {totals['total_prompt'] or 0:,}")
        print(f"  └─ Completion: {totals['total_completion'] or 0:,}")

        # 2. Model Breakdown
        print("\n🧠 --- MODEL DISTRIBUTION ---")
        breakdown = await conn.fetch('''
            SELECT model, layer, COUNT(*) as count, AVG(duration_ms) as avg_lat
            FROM usage_stats
            GROUP BY model, layer
            ORDER BY count DESC
        ''')
        
        for row in breakdown:
            lat = f"{row['avg_lat']:.0f}ms" if row['avg_lat'] > 0 else "N/A"
            print(f"[{row['layer']}] {row['model']:<20} | Count: {row['count']:<3} | Avg Lat: {lat}")

    await db.disconnect()
    print("\n")

if __name__ == "__main__":
    asyncio.run(show_stats())
