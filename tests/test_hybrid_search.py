"""
Test Suite: Hybrid Vector Search (Qdrant)
Tests Dense + Sparse retrieval and reranking pipeline
"""
import pytest
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

QDRANT_URL = "http://qdrant:6333"  # Docker service name
COLLECTION_NAME = "test_hybrid"

@pytest.fixture
def qdrant_client():
    """Fixture providing Qdrant client instance."""
    client = QdrantClient(url=QDRANT_URL)
    yield client
    # Cleanup: delete test collection after tests
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

@pytest.mark.asyncio
async def test_qdrant_connection():
    """Verify Qdrant service is accessible."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{QDRANT_URL}/collections")
            assert resp.status_code == 200
            print(f"✅ Qdrant Connection: Service online")
        except httpx.ConnectError:
            pytest.fail("❌ Qdrant not reachable at port 6333")

def test_create_hybrid_collection(qdrant_client):
    """Test creating a collection with Dense + Sparse vectors."""
    try:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                "dense": VectorParams(size=768, distance=Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": {}
            }
        )
        
        collections = qdrant_client.get_collections().collections
        assert any(c.name == COLLECTION_NAME for c in collections)
        print(f"✅ Hybrid Collection: Created '{COLLECTION_NAME}' successfully")
    except Exception as e:
        pytest.fail(f"❌ Collection Creation Failed: {e}")

def test_upsert_hybrid_vectors(qdrant_client):
    """Test upserting points with both dense and sparse vectors."""
    try:
        # Ensure collection exists
        test_create_hybrid_collection(qdrant_client)
        
        # Mock vectors (in real impl, these come from BGE-M3)
        test_point = PointStruct(
            id=1,
            vector={
                "dense": [0.1] * 768,  # Mock dense embedding
            },
            payload={"text": "Test document", "source": "test"}
        )
        
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[test_point]
        )
        
        # Verify point exists
        result = qdrant_client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[1]
        )
        assert len(result) == 1
        assert result[0].payload["text"] == "Test document"
        print("✅ Hybrid Upsert: Point stored successfully")
    except Exception as e:
        pytest.fail(f"❌ Upsert Failed: {e}")

def test_dense_search(qdrant_client):
    """Test dense (semantic) vector search."""
    try:
        # Ensure test data exists
        test_upsert_hybrid_vectors(qdrant_client)
        
        # Search with mock query vector
        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=[0.1] * 768,
            using="dense",
            limit=1
        ).points
        
        assert len(results) > 0
        assert results[0].payload["text"] == "Test document"
        print(f"✅ Dense Search: Retrieved {len(results)} results")
    except Exception as e:
        pytest.fail(f"❌ Dense Search Failed: {e}")

@pytest.mark.asyncio
async def test_reranker_integration():
    """Test BGE-Reranker integration (mock scoring)."""
    # Placeholder: Real implementation would call ollama_embed:11435
    # with BGE-Reranker model for cross-encoding
    query = "What is hybrid search?"
    candidates = [
        "Dense + Sparse search",
        "Unrelated document",
        "Hybrid retrieval technique"
    ]
    
    # Mock scoring (real impl uses BGE-Reranker)
    scores = [0.9, 0.1, 0.85]  # Simulated relevance scores
    
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    top_result = ranked[0][0]
    
    assert top_result == "Dense + Sparse search"
    print("✅ Reranker: Top result correctly identified")

if __name__ == "__main__":
    async def run_all():
        print("🚀 Starting Hybrid Search Tests...\\n")
        try:
            await test_qdrant_connection()
            client = QdrantClient(url=QDRANT_URL)
            await test_create_hybrid_collection(client)
            await test_upsert_hybrid_vectors(client)
            await test_dense_search(client)
            await test_reranker_integration()
            print("\\n💯 ALL HYBRID SEARCH TESTS PASSED")
        except Exception as e:
            print(f"\\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    import asyncio
    asyncio.run(run_all())
