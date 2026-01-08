import sys
import os
import sqlite3
from datetime import datetime

# Path to the database (in the parent folder)
DB_PATH = os.path.join(os.path.dirname(__file__), "../rag_memory.db")

def log_event(event_type, source, details):
    """Writes a log entry to the SQLite DB."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ensure table exists (just in case)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                source TEXT,
                details TEXT
            )
        """)
        
        # Insert Log
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO admin_logs (timestamp, event_type, source, details) VALUES (?, ?, ?, ?)",
            (now, event_type, source, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"   [Log Error] Could not write to DB: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python log_entry.py <TYPE> <SOURCE> <DETAILS>")
        sys.exit(1)
        
    log_event(sys.argv[1], sys.argv[2], sys.argv[3])