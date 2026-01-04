import pytest
import asyncio
from app.memory import QdrantVectorStore, save_interaction, retrieve_short_term_memory
from app.storage import MinioConnector
from app.database import db

@pytest.fixture(scope="module")
def storage():
    """Initializes Minio storage for testing."""
    return MinioConnector(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        bucket_name="test-bucket",
        secure=False
    )

@pytest.fixture(scope="module")
def memory(storage):
    """Initializes Qdrant memory for testing."""
    return QdrantVectorStore(
        storage=storage,
        host="localhost",
        port=6333
    )

@pytest.mark.asyncio
async def test_qdrant_omni_rag_flow(memory):
    """Verifies the full ingestion and search flow using Qdrant + MinIO."""
    test_text = "Omni-RAG separates vectors from blobs to optimize RAM and GPU usage."
    metadata = {"source": "test_logic", "type": "architecture"}
    
    # 1. Test Ingestion
    success = await memory.ingest(test_text, metadata)
    assert success is True, "Ingestion failed"
    
    # 2. Test Search (Retrieval)
    # Adding a small sleep to allow Qdrant to index (though Qdrant is usually fast)
    await asyncio.sleep(1)
    results = await memory.search("separation of vectors and blobs", top_k=1)
    
    assert len(results) > 0, "No results returned from search"
    assert "Omni-RAG" in results[0], f"Expected text not found in result: {results[0]}"

@pytest.mark.asyncio
async def test_short_term_memory_postgres():
    """Verifies that short-term conversation history still works in Postgres."""
    await db.connect()
    try:
        await save_interaction("user", "Hello logic test!")
        await save_interaction("assistant", "Logic test acknowledged.")
        
        history = await retrieve_short_term_memory()
        assert "USER: Hello logic test!" in history
        assert "ASSISTANT: Logic test acknowledged." in history
    finally:
        await db.disconnect()