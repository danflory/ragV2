import sqlite3
import os
from datetime import datetime

# Database Path (Same as your memory DB)
DB_PATH = os.path.join(os.path.dirname(__file__), "../rag_memory.db")

def init_log_table():
    """Ensures the admin_logs table exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            source TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_system_event(event_type: str, source: str, details: str):
    """
    Writes an event to the persistent log.
    Example: log_system_event("RESET", "CLI", "System restart initiated")
    """
    try:
        init_log_table()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # We manually insert timestamp to ensure it matches local system time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO admin_logs (timestamp, event_type, source, details)
            VALUES (?, ?, ?, ?)
        """, (now, event_type, source, details))
        
        conn.commit()
        conn.close()
        # print(f"   [System Log] 📝 Recorded: {event_type}")
    except Exception as e:
        print(f"   [System Log] ❌ Failed to log event: {e}")

if __name__ == "__main__":
    # Test run
    log_system_event("TEST", "Manual", "Testing logger...")