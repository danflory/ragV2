# 002_VECTOR_MEMORY.md
# STATUS: ACTIVE
# VERSION: 4.5.0 (Gravitas Command & Control / Telemetry Calibration)

## 1. OBJECTIVE
Implement the "Retrieval" in RAG with **Hybrid Vector Search**. The system uses Qdrant to store document embeddings and implements Dense + Sparse search for precision retrieval.

## 2. ARCHITECTURE
The system implements **Hybrid Vector Search** using **Qdrant** with **BGE-M3** for dual embedding (Dense + Sparse) and **BGE-Reranker** for precision hits.

### 2.1 The Components
1.  **`app/memory.py` (The Store):**
    * Class: `VectorStore`
    * Responsibilities: Initialize Qdrant client, Add documents, Query documents, Memory hygiene.
    * **IoC:** Injected into `app/container.py`.

2.  **`app/ingestor.py` (The Feeder):**
    * Responsibilities: Read MD/TXT files, chunk them into text blocks, and feed them to `VectorStore`.
    * **Memory Hygiene:** Prunes old vectors before ingestion to prevent "Vector Rot".

3.  **Embedding Pipeline:**
    * **GPU 1 (GTX 1060):** Dedicated embedding engine running multiple models
    * **Models:** `nomic-embed-text-v1.5`, `BAAI/bge-m3` (Dense+Sparse), `BAAI/bge-reranker-v2-m3`

## 3. HYBRID SEARCH DATA FLOW
1.  **User** asks a question.
2.  **Router** queries `VectorStore` with hybrid search.
3.  **Embedding Pipeline:** 
    * `nomic-embed-text-v1.5` generates dense vector
    * `BAAI/bge-m3` generates sparse vector (lexical keywords)
4.  **Qdrant Hybrid Search:** Combines dense + sparse results
5.  **Reranking:** `BAAI/bge-reranker-v2-m3` scores and sorts results
6.  **Context Injection:** Top results appended to LLM prompt

## 4. IMPLEMENTED INTERFACE
```python
class VectorStore:
    def __init__(self):
        """Initializes connection to Qdrant Docker Service & Local Embedder."""
    
    def add_texts(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        """Embeds and saves text chunks with circuit breaker for GPU resilience."""
        
    def search(self, query: str, n_results=5) -> list[str]:
        """Embeds query and searches Qdrant with circuit breaker resilience."""
        
    async def prune_source_vectors(self, source_id: str) -> int:
        """Memory Hygiene: Remove old vectors for a source before ingestion."""
        
    async def ingest_text(self, text: str, metadata: dict):
        """Dependency injection method for processing individual text documents."""
```

## 5. ADVANCED FEATURES
* **Circuit Breaker Pattern:** GPU embedding with CPU fallback for resilience
* **Memory Hygiene:** Automatic pruning of stale chunks to prevent vector rot
* **Parallel Processing:** GPU 1 dedicated to embeddings frees GPU 0 for generation
* **Hybrid Search:** Dense (semantic) + Sparse (lexical) for comprehensive retrieval
* **Reranking:** BGE-Reranker for precision hits
