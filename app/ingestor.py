import os
import logging
import uuid
import asyncio
from .interfaces import VectorMemory, ObjectStore

logger = logging.getLogger("AGY_INGESTOR")

class DocumentIngestor:
    """
    Scans the local docs/ directory and populates the Omni-RAG Memory.
    Updated for Phase 4.1: Uses async ingest() and separated storage.
    """
    def __init__(self, vector_store: VectorMemory, storage: ObjectStore):
        self.vector_store = vector_store
        self.storage = storage 
        from .config import config
        # Default docs path outside of container context might be different
        self.docs_path = config.DOCS_PATH

    def chunk_text(self, text: str, size: int = 1000) -> list[str]:
        """Simple break by size (1000 chars as per Phase 4.3 requirements)."""
        return [text[i:i+size] for i in range(0, len(text), size)]

    async def ingest_all(self):
        """Walks the docs/ folder and ingest everything."""
        if not self.vector_store:
            logger.error("❌ INGESTOR: No Vector Store connection.")
            return

        if not os.path.exists(self.docs_path):
            logger.warning(f"⚠️ INGESTOR: Directory {self.docs_path} not found.")
            return

        logger.info(f"🚀 INGESTOR: Scanning {self.docs_path}...")
        
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                # Support .md, .txt, and .py
                if file.endswith((".md", ".txt", ".py")):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.docs_path)
                    
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        chunks = self.chunk_text(content)
                        for i, chunk in enumerate(chunks):
                            metadata = {
                                "source": rel_path,
                                "chunk_index": i,
                                "file_type": file.split(".")[-1]
                            }
                            # Omni-RAG: Each chunk is uploaded separately
                            await self.vector_store.ingest(chunk, metadata)
                            
                        logger.info(f"✅ Ingested {file}: {len(chunks)} chunks")
                    except Exception as e:
                        logger.error(f"❌ Failed to ingest {file}: {e}")

        logger.info("✅ INGESTOR COMPLETE.")