#!/usr/bin/env python3
"""
Production-ready ingestion script for the Gravitas Grounded Research system.
This script ingests documents from multiple directories into the vector store.
"""
import sys
import os
import asyncio
import logging

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ingestor import DocumentIngestor
from app.container import container
from app.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("INGEST_SCRIPT")

async def main():
    """Main ingestion function."""
    logger.info("🚀 Starting document ingestion...")
    
    try:
        # Check if container is properly initialized
        if not container.memory or not container.storage:
            logger.error("❌ Container not properly initialized. Missing memory or storage.")
            sys.exit(1)
        
        # Create ingestor with container dependencies
        ingestor = DocumentIngestor(
            vector_store=container.memory,
            storage=container.storage
        )
        
        logger.info(f"📚 Configured paths: {ingestor.docs_path}")
        
        # Run ingestion
        await ingestor.ingest_all()
        
        logger.info("🎉 Document ingestion completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during ingestion: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Ingestion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Ingestion failed: {e}")
        sys.exit(1)
