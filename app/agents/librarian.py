import os
import logging
import shutil
import uuid
import asyncio
from typing import Dict, Any
from qdrant_client.http import models
from datetime import datetime

logger = logging.getLogger("AGY_LIBRARIAN")

class LibrarianAgent:
    """
    The Librarian: An autonomous agent for processing raw data imports.
    Follows the Night Shift architecture.
    """
    def __init__(self, container):
        self.container = container
        self.inbox_dir = "data/inbox"
        self.archive_dir = "data/archive"

        # Ensure directories exist
        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)

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

    async def process_inbox(self) -> Dict[str, Any]:
        """
        Scan data/inbox.
        1. Upload Raw Content to MinIO (Blob).
        2. Generate Summary.
        3. Ingest Summary to Qdrant (Index).
        4. Move file to data/archive.
        """
        if not os.path.exists(self.inbox_dir):
            return {"files_processed": 0, "status": "inbox_missing"}

        files = [f for f in os.listdir(self.inbox_dir) if os.path.isfile(os.path.join(self.inbox_dir, f))]
        processed_count = 0
        
        if not files:
            logger.info("Nothing to process in inbox.")
            return {"files_processed": 0, "status": "success"}

        for filename in files:
            file_path = os.path.join(self.inbox_dir, filename)
            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                
                if not raw_content.strip():
                    logger.warning(f"Skipping empty file: {filename}")
                    shutil.move(file_path, os.path.join(self.archive_dir, filename))
                    continue

                # 1. Upload Raw Content to MinIO (Blob)
                blob_key = f"raw_{uuid.uuid4().hex}"
                success = await self.container.storage.upload(blob_key, raw_content)
                if not success:
                    logger.error(f"❌ Failed to upload {filename} to storage.")
                    continue

                # 2. Generate Summary
                summary = await self.summarize(raw_content)

                # 3. Ingest Summary to Qdrant (Index)
                # Ensure the Qdrant payload links to the MinIO blob
                if self.container.memory and self.container.memory.client:
                    vector = await asyncio.to_thread(self.container.memory.embedder.encode, summary)
                    
                    payload = {
                        "source": filename,
                        "blob_key": blob_key,
                        "type": "librarian_processed",
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
                else:
                    logger.warning("⚠️ Memory not available, skipping vector indexing.")

                # 4. Move file to data/archive
                archive_path = os.path.join(self.archive_dir, filename)
                # Handle filename collisions in archive
                if os.path.exists(archive_path):
                    base, ext = os.path.splitext(filename)
                    archive_path = os.path.join(self.archive_dir, f"{base}_{uuid.uuid4().hex[:4]}{ext}")
                
                shutil.move(file_path, archive_path)
                processed_count += 1
                logger.info(f"✅ Librarian processed: {filename} -> {blob_key}")

            except Exception as e:
                logger.error(f"❌ Librarian failed on {filename}: {e}")

        return {"files_processed": processed_count, "status": "success"}
