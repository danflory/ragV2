import os
import logging
from .memory import memory

logger = logging.getLogger("AGY_INGEST")

class SimpleIngestor:
    def __init__(self, chunk_size=800, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def ingest_project(self):
        """Walks the directory and feeds ChromaDB."""
        valid_ext = ('.py', '.md', '.env', 'Dockerfile', '.yml', '.txt')
        exclude = {'.git', 'venv', '__pycache__', 'chroma_db', 'data'}

        logger.info("🚀 Starting ingestion...")
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file.endswith(valid_ext):
                    self._process_file(os.path.join(root, file))

    def _process_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Simple Chunking Logic
            chunks = [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size - self.overlap)]
            
            for idx, chunk in enumerate(chunks):
                doc_id = f"{path}_#_{idx}"
                memory.add_document(doc_id, chunk, {"path": path, "chunk": idx})
            
            logger.info(f"✅ Indexed: {path} ({len(chunks)} chunks)")
        except Exception as e:
            logger.error(f"❌ Failed {path}: {e}")

ingestor = SimpleIngestor()