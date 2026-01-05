import os
import time
import asyncio
import logging
import asyncpg
from datetime import datetime, timedelta

# Maintenance script for Antigravity Construction & Gravitas Research
# Purges local Reasoning Pipes (14 days) and executes Telemetry Pruning (60 days)

logger = logging.getLogger("Antigravity_MAINTENANCE")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def purge_old_files(directory, pattern, days=14):
    """Purges files in a directory matching a pattern if older than X days."""
    if not os.path.exists(directory):
        return

    now = time.time()
    cutoff = now - (days * 86400)
    count = 0

    for filename in os.listdir(directory):
        if pattern in filename:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                if os.path.getmtime(filepath) < cutoff:
                    try:
                        os.remove(filepath)
                        logger.info(f"🗑️ Purged old file: {filename}")
                        count += 1
                    except Exception as e:
                        logger.error(f"❌ Failed to purge {filename}: {e}")
    
    if count > 0:
        logger.info(f"✅ File maintenance complete: {count} files removed from {directory}")

async def prune_database():
    """Prunes Postgres telemetry and usage tables (60-day window)."""
    db_user = os.getenv("GRAVITAS_DB_USER", "Gravitas_user")
    db_pass = os.getenv("GRAVITAS_DB_PASS", "Gravitas_pass")
    db_name = os.getenv("GRAVITAS_DB_NAME", "Gravitas_db")
    db_host = os.getenv("GRAVITAS_DB_HOST", "localhost")
    db_port = os.getenv("GRAVITAS_DB_PORT", "5432")

    try:
        conn = await asyncpg.connect(
            user=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port
        )
        
        # 60-day retention
        cutoff_date = datetime.now() - timedelta(days=60)
        
        # Prune Usage Stats
        res_usage = await conn.execute("DELETE FROM usage_stats WHERE timestamp < $1", cutoff_date)
        count_usage = int(res_usage.split()[1]) if res_usage.startswith("DELETE") else 0
        
        # Prune Telemetry
        res_tele = await conn.execute("DELETE FROM system_telemetry WHERE timestamp < $1", cutoff_date)
        count_tele = int(res_tele.split()[1]) if res_tele.startswith("DELETE") else 0
        
        logger.info(f"📈 Database Pruning: {count_usage} usage rows and {count_tele} telemetry rows removed.")
        await conn.close()
    except Exception as e:
        logger.error(f"❌ Database Pruning Failed: {e}")

async def main():
    logger.info("🛠️ Starting Antigravity System Maintenance...")
    
    # Target directories and patterns
    targets = [
        # (directory, pattern, days)
        (".", ".log", 14),
        (".", ".bak", 1), # Backups purge faster (1 day)
        ("docs/journals", "_executive.md", 14),
        ("docs/journals", "_thoughts.md", 14),
        ("docs/journals", "AntigravityThoughtLog_", 14),
        ("docs", "TEST_AUDIT_", 14),
    ]

    for directory, pattern, days in targets:
        purge_old_files(directory, pattern, days)
    
    # 2. Database Pruning (Async)
    await prune_database()
    logger.info("✅ All maintenance tasks complete.")


if __name__ == "__main__":
    asyncio.run(main())
