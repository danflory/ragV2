import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models

def fix():
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "gravitas_knowledge"
    
    print(f"Checking collection: {collection_name}")
    if client.collection_exists(collection_name):
        print("Collection exists. Deleting...")
        client.delete_collection(collection_name)
    
    print("Creating collection with size 384 (all-MiniLM-L6-v2)...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384, 
            distance=models.Distance.COSINE
        ),
    )
    print("✅ Collection recreated.")

if __name__ == "__main__":
    fix()
