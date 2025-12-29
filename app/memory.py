import os
import shutil
import logging
import asyncio
import json
import sqlite3
import chromadb
from datetime import datetime
from chromadb.config import Settings
from .config import CONFIG

# FIX: Use getattr() for class attributes, not .get()
# Also fixed variable name to match config.py (CHROMA_PATH vs CHROMA_DB_PATH)
CHROMA_PATH = getattr(CONFIG, "CHROMA_PATH", "./rag_local/chroma_db")
HISTORY_LIMIT = getattr(CONFIG, "CHAT_HISTORY_LIMIT", 25)

logger = logging.getLogger("AGY_Memory")

# Ensure DB Directory Exists
if not os.path.exists(CHROMA_PATH):
    os.makedirs(CHROMA_PATH)

# Initialize Clients
try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name="agy_knowledge")
    logger.info(f"✅ ChromaDB loaded at {CHROMA_PATH}")
except Exception as e:
    logger.error(f"❌ ChromaDB Init Failed: {e}")
    collection = None

# --- SQLite for Chat History ---
DB_FILE = "chat_history.db"

def init_sqlite():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, role TEXT, content TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_sqlite()

async def save_interaction(role: str, content: str):
    """Saves a single message to SQLite history."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO history (role, content, timestamp) VALUES (?, ?, ?)", 
                  (role, content, datetime.now()))
        
        # Prune old history
        c.execute(f"DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT {HISTORY_LIMIT})")
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Save History Error: {e}")

async def retrieve_memory_context(query: str) -> str:
    """
    Retrieves recent chat history (SQLite) + relevant docs (ChromaDB).
    """
    context_str = ""
    
    # 1. Get Recent Chat History
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"SELECT role, content FROM history ORDER BY id ASC")
        rows = c.fetchall()
        conn.close()
        
        history_text = "\n".join([f"{r[0].upper()}: {r[1]}" for r in rows])
        context_str += f"--- CHAT HISTORY ---\n{history_text}\n\n"
    except Exception as e:
        logger.error(f"History Retrieve Error: {e}")

    # 2. Get RAG Documents (if meaningful query)
    if collection and len(query) > 5:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=3
            )
            if results["documents"]:
                docs = results["documents"][0]
                context_str += "--- RELEVANT DOCUMENTS ---\n"
                context_str += "\n".join(docs)
                context_str += "\n"
        except Exception as e:
            logger.error(f"RAG Retrieve Error: {e}")

    return context_str