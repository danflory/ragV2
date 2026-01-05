#!/usr/bin/env python3
"""
Test script to verify the updated ingestor can handle multiple directories.
"""
import sys
import os
import asyncio

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ingestor import DocumentIngestor
from app.config import config

class MockVectorStore:
    """Mock vector store for testing."""
    def __init__(self):
        self.ingested_items = []
    
    async def ingest(self, content, metadata):
        self.ingested_items.append({
            'content': content,
            'metadata': metadata
        })
        print(f"✅ Ingested: {metadata['source']} (chunk {metadata['chunk_index']})")

class MockStorage:
    """Mock storage for testing."""
    pass

async def main():
    print("🚀 Testing DocumentIngestor with multiple directories...")
    
    # Create mock dependencies
    mock_vector_store = MockVectorStore()
    mock_storage = MockStorage()
    
    # Create ingestor with updated config
    ingestor = DocumentIngestor(vector_store=mock_vector_store, storage=mock_storage)
    
    print(f"📚 Configured paths: {ingestor.docs_path}")
    
    # Run ingestion
    await ingestor.ingest_all()
    
    print(f"🎉 Ingestion complete! Processed {len(mock_vector_store.ingested_items)} chunks")

if __name__ == "__main__":
    asyncio.run(main())
