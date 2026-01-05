import os
import time
import logging
from datetime import datetime, timedelta

# Maintenance script for Gravitas Grounded Research
# Purges old logs, backups, and journals older than 14 days (2 weeks)

logger = logging.getLogger("Gravitas_MAINTENANCE")
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
        logger.info(f"✅ Maintenance complete: {count} files removed from {directory}")

def main():
    logger.info("🛠️ Starting System Maintenance...")
    
    # Target directories and patterns
    targets = [
        # (directory, pattern, days)
        (".", ".log", 14),
        (".", ".bak", 1), # Backups purge faster (1 day)
        ("docs/journals", "_executive.md", 14), # Dated executive journals
        ("docs/journals", "_thoughts.md", 14),  # Dated thought logs
        ("docs", "TEST_AUDIT_", 14),
    ]

    for directory, pattern, days in targets:
        purge_old_files(directory, pattern, days)

if __name__ == "__main__":
    main()
