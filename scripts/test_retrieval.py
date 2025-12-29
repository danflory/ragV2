import os
import chromadb
from chromadb.utils import embedding_functions

# 1. Setup paths (Same logic as ingestion)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(ROOT_DIR, "data", "chroma_db")

# 2. Connect to the brain
default_ef = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name="local_knowledge", embedding_function=default_ef)

def search_knowledge(query_text):
    print(f"\n🔍 Searching for: '{query_text}'")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=1 # Give me the single best match
    )
    
    # Print results
    for i, doc in enumerate(results['documents'][0]):
        title = results['metadatas'][0][i]['title']
        print(f"✅ Found match in [{title}]:")
        print(f"   '{doc}'")

if __name__ == "__main__":
    # Test 1: Direct Match
    search_knowledge("How much VRAM does the Titan have?")
    
    # Test 2: Conceptual Match (The word 'GPU' isn't in the question)
    search_knowledge("What hardware should I use for local LLMs?")