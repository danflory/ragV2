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
        """Embeds and saves text chunks."""
        if not texts: return

        try:
            embeddings = self.embedder.encode(texts).tolist()
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"💾 MEMORY: Stored {len(texts)} chunks.")
        except Exception as e:
            logger.error(f"❌ ADD ERROR: {e}")

    def search(self, query: str, n_results=5) -> list[str]:
        """Embeds query and searches Chroma."""
        try:
            query_embedding = self.embedder.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"❌ SEARCH ERROR: {e}")
            return []