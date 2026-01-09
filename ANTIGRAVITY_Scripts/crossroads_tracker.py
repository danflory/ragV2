import sqlite3
import re
import os
import sys
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Find the project root by looking for .git or going up until we find docs/
current = SCRIPT_DIR
while current != os.path.dirname(current):
    if os.path.exists(os.path.join(current, ".git")) or os.path.exists(os.path.join(current, "docs")):
        PROJECT_ROOT = current
        break
    current = os.path.dirname(current)
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..")) # Fallback

DB_PATH = os.path.join(PROJECT_ROOT, "docs", "journals", "crossroads.db")
EXECUTIVE_DIR = os.path.join(PROJECT_ROOT, "docs", "journals", "executive")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategic_crossroads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            description TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'RESOLVED', 'DISMISSED')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn

def sync_crossroads():
    today_str = datetime.now().strftime("%Y-%m-%d")
    journal_path = os.path.join(EXECUTIVE_DIR, f"{today_str}_executive.md")
    
    if not os.path.exists(journal_path):
        print(f"No executive journal found for {today_str}.")
        return

    with open(journal_path, 'r') as f:
        content = f.read()

    # Extract Crossroads using Regex
    # Looking for: ### Strategic Crossroads\n( - .* \n)*
    matches = re.findall(r"### Strategic Crossroads(.*?)(?=\n##|---|$)", content, re.DOTALL)
    
    conn = init_db()
    cursor = conn.cursor()
    
    for match in matches:
        items = re.findall(r"- (.*)", match)
        for item in items:
            description = item.strip()
            if description:
                cursor.execute("""
                    INSERT INTO strategic_crossroads (session_date, description)
                    VALUES (?, ?)
                    ON CONFLICT(description) DO NOTHING
                """, (today_str, description))
    
    conn.commit()
    print(f"✅ Synced crossroads from {journal_path}")
    conn.close()

def show_status():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, session_date, description FROM strategic_crossroads WHERE status = 'OPEN'")
    rows = cursor.fetchall()
    
    if not rows:
        print("\n✨ All strategic crossroads are handled.")
    else:
        print("\n🚩 UNHANDLED STRATEGIC CROSSROADS:")
        for row in rows:
            print(f"[{row[0]}] ({row[1]}) {row[2]}")
    conn.close()

def resolve_item(item_id):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE strategic_crossroads SET status = 'RESOLVED', updated_at = ? WHERE id = ?", (datetime.now(), item_id))
    if cursor.rowcount > 0:
        print(f"✅ Item [{item_id}] marked as RESOLVED")
    else:
        print(f"❌ Item [{item_id}] not found")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 crossroads_tracker.py [--sync | --status | --resolve <id>]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "--sync":
        sync_crossroads()
    elif cmd == "--status":
        show_status()
    elif cmd == "--resolve" and len(sys.argv) > 2:
        resolve_item(sys.argv[2])
    else:
        print("Invalid command or missing ID")
