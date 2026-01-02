import logging
import os
import chromadb
from datetime import datetime
from sentence_transformers import SentenceTransformer
from .config import config

from .database import db

logger = logging.getLogger("AGY_MEMORY")

# --- POSTGRES: SHORT-TERM CONVERSATION HISTORY ---

async def save_interaction(role: str, content: str):
    """Saves a single message to Postgres history."""
    if not db.is_ready():
        logger.warning("⚠️ DB NOT READY: Skipping history save.")
        return

    try:
        async with db.pool.acquire() as conn:
            await conn.execute("INSERT INTO history (role, content, timestamp) VALUES ($1, $2, $3)", 
                              role, content, datetime.now())
            
            # Prune old history (Configurable limit)
            limit = 25 
            await conn.execute(f"DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT {limit})")
    except Exception as e:
        logger.error(f"❌ HISTORY ERROR: {e}")

async def retrieve_short_term_memory() -> str:
    """Retrieves recent chat history formatted for the LLM."""
    if not db.is_ready():
        return ""

    try:
        async with db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT role, content FROM history ORDER BY id ASC")
            
        if not rows:
            return ""
            
        history_text = "\n".join([f"{r['role'].upper()}: {r['content']}" for r in rows])
        return f"--- CHAT HISTORY ---\n{history_text}\n"
    except Exception as e:
        logger.error(f"❌ RETRIEVE ERROR: {e}")
        return ""

# --- CHROMA: LONG-TERM VECTOR MEMORY ---
class VectorStore:
    def __init__(self):
        """
        Initializes connection to ChromaDB Docker Service & Local Embedder.
        """
        self.client = None
        self.collection = None
        self.embedder = None
        self._initialize_connection()

    def _initialize_connection(self):
        # 1. Connect to Docker Service (Not local file!)
        logger.info(f"🔌 CONNECTING TO MEMORY at {config.CHROMA_URL}...")
        try:
            self.client = chromadb.HttpClient(
                host="chroma_db", # Internal docker hostname
                port=8000
            )
            
            # 2. Get/Create Collection
            self.collection = self.client.get_or_create_collection(
                name=config.CHROMA_COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("✅ VECTOR DB CONNECTED.")
        except Exception as e:
            logger.error(f"❌ VECTOR DB FAILURE: {e}")
            # We don't raise here, instead we allow the app to boot without memory if it fails
            # But the container.py should handle this if it wants to be strict.
            self.client = None
            self.collection = None

        # 3. Load Embedding Model (Runs on GPU if available)
        if self.client:
            logger.info("🧠 LOADING EMBEDDING MODEL (all-MiniLM-L6-v2)...")
            try:
                self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ EMBEDDING MODEL READY.")
            except Exception as e:
                logger.critical(f"❌ MODEL LOAD FAILED: {e}")
                self.embedder = None

    def add_texts(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        """Embeds and saves text chunks with circuit breaker for GPU resilience."""
        if not texts: return

        # Circuit Breaker: Try GPU embedding first, fallback to CPU
        embeddings = None
        embedding_device = "GPU"

        try:
            if self.embedder:
                embeddings = self.embedder.encode(texts).tolist()
            else:
                raise RuntimeError("Embedder not initialized")
        except Exception as gpu_error:
            logger.warning(f"⚠️ GPU EMBEDDING FAILED: {gpu_error}")
            embedding_device = "CPU"

            # Fallback to CPU embedding
            try:
                cpu_embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                embeddings = cpu_embedder.encode(texts).tolist()
                logger.info("✅ CPU EMBEDDING FALLBACK: Successfully used CPU for embedding")
            except Exception as cpu_error:
                logger.error(f"❌ CPU EMBEDDING FAILED: {cpu_error}")
                raise RuntimeError(f"Embedding failed on both GPU and CPU: GPU error: {gpu_error}, CPU error: {cpu_error}")

        # Store in vector database
        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"💾 MEMORY: Stored {len(texts)} chunks via {embedding_device}.")
        except Exception as e:
            logger.error(f"❌ VECTOR DB ADD ERROR: {e}")
            raise

    def search(self, query: str, n_results=5) -> list[str]:
        """Embeds query and searches Chroma with circuit breaker resilience."""
        try:
            # Circuit Breaker: Try GPU embedding first, fallback to CPU
            if self.embedder:
                try:
                    query_embedding = self.embedder.encode([query]).tolist()
                except Exception as gpu_error:
                    logger.warning(f"⚠️ GPU SEARCH EMBEDDING FAILED: {gpu_error}, falling back to CPU")
                    cpu_embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                    query_embedding = cpu_embedder.encode([query]).tolist()
            else:
                # No embedder initialized, use CPU
                cpu_embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                query_embedding = cpu_embedder.encode([query]).tolist()

            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"❌ SEARCH ERROR: {e}")
            return []

    async def prune_source_vectors(self, source_id: str) -> int:
        """
        Memory Hygiene: Remove old vectors for a source before ingestion.
        Prevents "Vector Rot" by ensuring only current content is retained.

        Args:
            source_id: The source identifier (e.g., "app/main.py")

        Returns:
            Number of chunks deleted
        """
        try:
            # Get all documents with their metadata
            results = self.collection.get()

            if not results or not results.get('ids'):
                return 0

            # Find IDs that match the source_id
            ids_to_delete = []
            for i, metadata in enumerate(results.get('metadatas', [])):
                if metadata and metadata.get('source') == source_id:
                    ids_to_delete.append(results['ids'][i])

            if not ids_to_delete:
                return 0

            # Delete the old chunks
            self.collection.delete(ids=ids_to_delete)
            logger.info(f"🧹 PRUNED: {len(ids_to_delete)} old chunks for {source_id}")

            return len(ids_to_delete)

        except Exception as e:
            logger.error(f"❌ PRUNE ERROR: Failed to prune {source_id}: {e}")
            return 0

    async def ingest_text(self, text: str, metadata: dict):
        """
        Dependency injection method for processing individual text documents.
        Wraps the synchronous add_texts method for async compatibility.
        Part of the system's data processing pipeline.
        """
        import uuid
        import asyncio

        # Memory Hygiene: Prune old vectors before ingestion
        source_id = metadata.get('source', 'unknown')
        pruned_count = await self.prune_source_vectors(source_id)

        # Generate unique ID for this document
        doc_id = f"{source_id}_{uuid.uuid4().hex[:8]}"

        # Convert to list format expected by add_texts
        texts = [text]
        metadatas = [metadata]
        ids = [doc_id]

        # Execute synchronously in thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.add_texts, texts, metadatas, ids)

        logger.info(f"📥 INGESTED: {source_id} ({len(text)} chars, pruned {pruned_count} old chunks)")
