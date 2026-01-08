#!/usr/bin/env python3
import asyncio
import os
import sys

# Ensure we can import app components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.database import db

class UsageStatsTool:
    """Tool for retrieving system usage statistics from the database."""
    
    def __init__(self):
        pass

    async def execute(self):
        await db.connect()
        if not db.is_ready():
            print("❌ Could not connect to database.")
            return False, "Database connection failed"

        try:
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
                total_reqs = totals['total_requests'] or 0
                total_prompt = totals['total_prompt'] or 0
                total_completion = totals['total_completion'] or 0
                
                print(f"Total Requests: {total_reqs}")
                print(f"Total Tokens:   {total_prompt + total_completion:,}")
                print(f"  └─ Prompt:     {total_prompt:,}")
                print(f"  └─ Completion: {total_completion:,}")

                # 2. Model Breakdown
                print("\n🧠 --- MODEL DISTRIBUTION ---")
                breakdown = await conn.fetch('''
                    SELECT model, layer, COUNT(*) as count, AVG(duration_ms) as avg_lat
                    FROM usage_stats
                    GROUP BY model, layer
                    ORDER BY count DESC
                ''')
                
                for row in breakdown:
                    lat = f"{row['avg_lat']:.0f}ms" if row['avg_lat'] and row['avg_lat'] > 0 else "N/A"
                    print(f"[{row['layer']}] {row['model']:<20} | Count: {row['count']:<3} | Avg Lat: {lat}")

            return True, "Stats retrieved"
        except Exception as e:
            print(f"❌ Error retrieving stats: {e}")
            return False, str(e)
        finally:
            await db.disconnect()

if __name__ == "__main__":
    tool = UsageStatsTool()
    asyncio.run(tool.execute())
