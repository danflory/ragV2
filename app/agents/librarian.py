import os
import logging
import shutil
import uuid
import asyncio
from typing import Dict, Any
from qdrant_client.http import models
from datetime import datetime

logger = logging.getLogger("Gravitas_LIBRARIAN")

class LibrarianAgent:
    """
    The Librarian: An autonomous agent for processing documentation and code.
    Scans docs/ and app/ directories, generates AI summaries, and indexes them.
    Follows the Night Shift architecture.
    """
    def __init__(self, container):
        self.container = container
        from ..config import config
        self.scan_dirs = config.DOCS_PATH  # Uses same paths as Ingestor

    async def summarize(self, text: str) -> str:
        """
        Uses L1 (Reflex) to generate a dense summary/abstract of the content.
        """
        prompt = f"TASK: Compress the following text into a high-density summary for vector retrieval. Focus on key entities, technical specs, and core intent.\nTEXT: {text[:4000]}"
        try:
            summary = await self.container.l1_driver.generate(prompt)
            # If L1 fails or returns error tag, use a fallback
            if summary.startswith("[L1 Error") or "ESCALATE" in summary:
                logger.warning(f"L1 summary failed: {summary}")
                return text[:500] + "..." # Fallback to snippet
            return summary
        except Exception as e:
            logger.error(f"Error in summarize: {e}")
            return text[:500] + "..."

    async def process_docs(self) -> Dict[str, Any]:
        """
        Scan docs/ and app/ directories.
        1. Upload Raw Content to MinIO (Blob).
        2. Generate AI Summary using L1.
        3. Ingest Summary to Qdrant (Index).
        """
        paths = self.scan_dirs if isinstance(self.scan_dirs, list) else [self.scan_dirs]
        processed_count = 0
        chunks_ingested = 0
        
        for path in paths:
            if not os.path.exists(path):
                logger.warning(f"⚠️ LIBRARIAN: Directory {path} not found.")
                continue

            logger.info(f"🚀 LIBRARIAN: Scanning {path}...")
            
            for root, _, files in os.walk(path):
                # Skip __pycache__ and other noise
                if "__pycache__" in root or ".git" in root:
                    continue

                for file in files:
                    # Support .md, .txt, and .py
                    if file.endswith((".md", ".txt", ".py")):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, path)
                        
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                raw_content = f.read()
                                
                            if not raw_content.strip():
                                continue

                            # 1. Upload Raw Content to MinIO (Blob)
                            blob_key = f"librarian_{uuid.uuid4().hex}"
                            success = await self.container.storage.upload(blob_key, raw_content)
                            if not success:
                                logger.error(f"❌ Failed to upload {rel_path} to storage.")
                                continue

                            # 2. Generate AI Summary
                            summary = await self.summarize(raw_content)

                            # 3. Ingest Summary to Qdrant (Index)
                            if self.container.memory and self.container.memory.client:
                                vector = await asyncio.to_thread(self.container.memory.embedder.encode, summary)
                                
                                payload = {
                                    "source": rel_path,
                                    "blob_key": blob_key,
                                    "type": "librarian_ai_summary",
                                    "summary_preview": summary[:500],
                                    "timestamp": datetime.now().isoformat()
                                }
                                
                                self.container.memory.client.upsert(
                                    collection_name=self.container.memory.collection_name,
                                    points=[
                                        models.PointStruct(
                                            id=str(uuid.uuid4()),
                                            vector=vector.tolist(),
                                            payload=payload
                                        )
                                    ]
                                )
                                chunks_ingested += 1
                            else:
                                logger.warning("⚠️ Memory not available, skipping vector indexing.")

                            processed_count += 1
                            logger.info(f"✅ Librarian processed: {rel_path} -> {blob_key}")

                        except Exception as e:
                            logger.error(f"❌ Librarian failed on {rel_path}: {e}")

        return {
            "files_processed": processed_count, 
            "chunks_ingested": chunks_ingested,
            "status": "success"
        }
