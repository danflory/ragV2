import logging
import uuid
import asyncio
from typing import List, Dict, Optional, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from datetime import datetime

from .interfaces import VectorMemory, ObjectStore
from .config import config
from .database import db

logger = logging.getLogger("Gravitas_MEMORY")

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

# --- QDRANT: LONG-TERM GRAVITAS GROUNDED RESEARCH MEMORY ---

class QdrantVectorStore(VectorMemory):
    """Implementation of VectorMemory using Qdrant (Indices) and ObjectStore (Blobs)."""

    def __init__(self, storage: ObjectStore, host: str = "localhost", port: int = 6333):
        self.storage = storage
        self.collection_name = "gravitas_knowledge"
        self.embedding_model_name = 'all-MiniLM-L6-v2'
        self.vector_size = 384 # For all-MiniLM-L6-v2
        
        logger.info(f"🔌 CONNECTING TO QDRANT at {host}:{port}...")
        self.client = QdrantClient(host=host, port=port)
        
        logger.info(f"🧠 LOADING EMBEDDING MODEL ({self.embedding_model_name})...")
        self.embedder = SentenceTransformer(self.embedding_model_name)
        
        self._ensure_collection()

    def _ensure_collection(self):
        """Creates the Qdrant collection if it doesn't exist."""
        try:
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size, 
                        distance=models.Distance.COSINE
                    ),
                )
                logger.info(f"✅ Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"❌ QDRANT COLLECTION ERROR: {e}")

    async def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Gravitas Grounded Research Search:
        1. Embed query.
        2. Search Qdrant for indices.
        3. Fetch blobs from Storage using blob_key.
        """
        try:
            # 1. Embed Query (using to_thread for sync embedder)
            query_vector = await asyncio.to_thread(self.embedder.encode, query)
            
            # 2. Search Qdrant
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector.tolist(),
                limit=top_k
            )
            
            # 3. Fetch Blobs
            results = []
            for point in response.points:
                blob_key = point.payload.get("blob_key")
                if blob_key:
                    content = await self.storage.get(blob_key)
                    if content:
                        results.append(content)
            
            return results
        except Exception as e:
            logger.error(f"❌ SEARCH ERROR: {e}")
            return []

    async def ingest(self, text: str, metadata: Dict[str, Any]) -> bool:
        """
        Gravitas Grounded Research Ingestion:
        1. Upload text to MinIO (Blob).
        2. Embed text.
        3. Upsert Vector + Metadata (Index) to Qdrant.
        """
        try:
            # 1. Generate Blob Key and Upload
            blob_key = f"blob_{uuid.uuid4().hex}"
            if not await self.storage.upload(blob_key, text):
                logger.error("❌ INGESTION FAILED: Could not upload to storage.")
                return False
            
            # 2. Embed Text
            vector = await asyncio.to_thread(self.embedder.encode, text)
            
            # 3. Create Payload (Do NOT store raw text here as per Constitutional Law)
            payload = metadata.copy()
            payload["blob_key"] = blob_key
            payload["timestamp"] = datetime.now().isoformat()
            
            # 4. Upsert to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector.tolist(),
                        payload=payload
                    )
                ]
            )
            
            logger.info(f"💾 INGESTED: {metadata.get('source', 'unknown')} blob_key={blob_key}")
            return True
        except Exception as e:
            logger.error(f"❌ INGESTION ERROR: {e}")
            return False
