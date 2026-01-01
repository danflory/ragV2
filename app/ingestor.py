import os
import logging
import uuid
from .memory import VectorStore

logger = logging.getLogger("AGY_INGESTOR")

class DocumentIngestor:
    """
    Scans the local docs/ directory and populates the Vector Memory.
    """
    def __init__(self, vector_store: VectorStore):
        self.store = vector_store
        from .config import config
        self.docs_path = config.DOCS_PATH

    def chunk_text(self, text: str, size: int = 1000) -> list[str]:
        """Simple break by size for now."""
        return [text[i:i+size] for i in range(0, len(text), size)]

    def ingest_all(self):
        """Walks the docs/ folder and ingest everything."""
        if not self.store:
            logger.error("❌ INGESTOR: No Vector Store connection.")
            return

        if not os.path.exists(self.docs_path):
            logger.warning(f"⚠️ INGESTOR: Directory {self.docs_path} not found.")
            return

        logger.info(f"🚀 INGESTOR: Scanning {self.docs_path}...")
        
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.docs_path)
                    
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        chunks = self.chunk_text(content)
                        metadatas = [{"source": rel_path} for _ in chunks]
                        ids = [f"{rel_path}_{uuid.uuid4().hex[:8]}" for _ in chunks]
                        
                        self.store.add_texts(chunks, metadatas, ids)
                        logger.info(f"   + Ingested {file} ({len(chunks)} chunks)")
                    except Exception as e:
                        logger.error(f"   - Failed to ingest {file}: {e}")

        logger.info("✅ INGESTOR COMPLETE.")