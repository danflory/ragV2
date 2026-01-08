#!/usr/bin/env python3
import sys
import os
import asyncio
import logging

# Ensure we can import app components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.ingestor import DocumentIngestor
from app.container import container
from app.config import config

logger = logging.getLogger("LibrarianIngestTool")

class IngestionTool:
    """Tool for ingesting documents into the vector store."""
    
    def __init__(self):
        self.ingestor = None

    async def execute(self):
        """Main ingestion function."""
        logger.info("🚀 Starting document ingestion...")
        
        try:
            # Check if container is properly initialized
            if not container.memory or not container.storage:
                logger.error("❌ Container not properly initialized. Missing memory or storage.")
                return False, "Container missing memory or storage"
            
            # Create ingestor with container dependencies
            self.ingestor = DocumentIngestor(
                vector_store=container.memory,
                storage=container.storage
            )
            
            logger.info(f"📚 Configured paths: {self.ingestor.docs_path}")
            
            # Run ingestion
            await self.ingestor.ingest_all()
            
            logger.info("🎉 Document ingestion completed successfully!")
            return True, "Ingestion completed"
            
        except Exception as e:
            logger.error(f"❌ Error during ingestion: {e}")
            return False, str(e)

if __name__ == "__main__":
    tool = IngestionTool()
    try:
        asyncio.run(tool.execute())
    except KeyboardInterrupt:
        logger.info("🛑 Ingestion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Ingestion failed: {e}")
        sys.exit(1)
