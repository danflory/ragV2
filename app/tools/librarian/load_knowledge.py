import json
import chromadb
from chromadb.utils import embedding_functions
import os

# Get the absolute path of the project root (one level up from this script)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(ROOT_DIR, "data", "knowledge.json")
CHROMA_PATH = os.path.join(ROOT_DIR, "data", "chroma_db")

# 2. Initialize Chroma and Embedding Function
# This uses a light-weight model that runs locally on your machine
default_ef = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="local_knowledge", embedding_function=default_ef)

def ingest_data():
    if not os.path.exists(DATA_PATH):
        print("Knowledge file not found!")
        return

    with open(DATA_PATH, 'r') as f:
        data = json.load(f)

    # Prepare data for Chroma
    documents = [item['content'] for item in data]
    metadatas = [{"title": item['title']} for item in data]
    ids = [item['id'] for item in data]

    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Successfully ingested {len(documents)} documents into ChromaDB.")

if __name__ == "__main__":
    ingest_data()