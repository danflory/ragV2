import os
import logging
import uuid
import asyncio
from .interfaces import VectorMemory, ObjectStore

logger = logging.getLogger("Gravitas_Ingestor")

class DocumentIngestor:
    """
    Scans the local docs/ directory and populates the Gravitas Grounded Research Memory.
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

        # Handle both single path (string) and multiple paths (list)
        paths = self.docs_path if isinstance(self.docs_path, list) else [self.docs_path]
        
        for path in paths:
            if not os.path.exists(path):
                logger.warning(f"⚠️ INGESTOR: Directory {path} not found.")
                continue

            logger.info(f"🚀 INGESTOR: Scanning {path}...")
            
            for root, _, files in os.walk(path):
                for file in files:
                    # Support .md, .txt, and .py
                    if file.endswith((".md", ".txt", ".py")):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, path)
                        
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
                                # Gravitas Grounded Research: Each chunk is uploaded separately
                                await self.vector_store.ingest(chunk, metadata)
                                
                            logger.info(f"✅ Ingested {file}: {len(chunks)} chunks")
                        except Exception as e:
                            logger.error(f"❌ Failed to ingest {file}: {e}")

        logger.info("✅ INGESTOR COMPLETE.")
