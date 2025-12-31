# 002_VECTOR_MEMORY.md
# STATUS: DRAFT
# FEATURE: Local Vector Store (ChromaDB)

## 1. OBJECTIVE
Implement the "Retrieval" in RAG. We need a persistent local database to store document embeddings so the Agent can "remember" context from your files.

## 2. ARCHITECTURE
We will use **ChromaDB** (running locally in Docker or embedded) because it is lightweight and requires no external API keys.

### 2.1 The Components
1.  **`app/memory.py` (The Store):**
    * Class: `VectorStore`
    * Responsibilities: Initialize Chroma client, Create collections, Add documents, Query documents.
    * **IoC:** Injected into `app/container.py`.

2.  **`app/ingest.py` (The Feeder):**
    * Responsibilities: Read PDF/MD/TXT files, chunk them into small text blocks, and feed them to `VectorStore`.

3.  **Embedding Model:**
    * We will use a **Local Embedding Model** (via `sentence-transformers`) to turn text into numbers.
    * *Decision Point:* Using `sentence-transformers/all-MiniLM-L6-v2` runs on CPU/GPU directly in Python, which is faster/more stable than hitting the Ollama API for every chunk.

## 3. DATA FLOW
1.  **User** uploads `docs/manual.pdf`.
2.  **Reflex** triggers `ingest_file("docs/manual.pdf")`.
3.  **Ingest** reads file -> splits into 500-token chunks.
4.  **VectorStore** calculates embeddings -> saves to `./chroma_db/`.
5.  **Router** (later): When User asks a question, we query `VectorStore` first, append results to Prompt, then send to L2.

## 4. PROPOSED INTERFACE
```python
class VectorStore:
    def __init__(self, persistence_path: str):
        ...
    
    def add_texts(self, texts: list[str], metadatas: list[dict]):
        """Embeds and saves text chunks."""
        ...
        
    def search(self, query: str, n_results=5) -> list[str]:
        """Returns the top N relevant text chunks."""
        ...
```

## 5. RISKS & MITIGATIONS
* **Risk:** Embedding 100 files takes too long.
* **Mitigation:** We will implement batch processing in `ingest.py`.
* **Risk:** Docker Permissions on `./chroma_db/`.
* **Mitigation:** We have already `gitignored` this folder, but we must ensure the Docker container runs as a user with write access to the volume.