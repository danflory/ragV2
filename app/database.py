import chromadb
from chromadb.config import Settings
import os

# Define the path to your data folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

def get_db_client():
    # This connects to the actual files on your disk
    client = chromadb.PersistentClient(path=DATA_DIR)
    return client

def log_inference(status, query, cost=0.0):
    # For now, a simple heartbeat log
    print(f"[LOG] {status}: {query} (Cost: ${cost})")

# Test Heartbeat
if __name__ == "__main__":
    try:
        client = get_db_client()
        print(f"✅ ChromaDB heartbeat success! Data stored at: {DATA_DIR}")
        print(f"Current collections: {client.list_collections()}")
    except Exception as e:
        print(f"❌ ChromaDB heartbeat failed: {e}")