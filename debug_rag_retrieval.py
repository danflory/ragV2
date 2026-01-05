"""
Quick RAG Debug Script

Tests a specific query to see what context is being retrieved from Qdrant.
"""

import asyncio
import sys
sys.path.insert(0, '/app')

from app.container import container


async def test_query(query):
    """Test what context is retrieved for a specific query."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")
    
    try:
        # Initialize memory if needed
        if container.memory:
            # Search for relevant documents
            docs = await container.memory.search(query, top_k=5)
            
            if docs:
                print(f"✅ Retrieved {len(docs)} chunks from RAG:")
                print("-" * 60)
                for i, doc in enumerate(docs, 1):
                    print(f"\n[Chunk {i}]")
                    print(doc[:300] + "..." if len(doc) > 300 else doc)
                    print("-" * 60)
            else:
                print("❌ No chunks retrieved from RAG")
        else:
            print("❌ Memory system not initialized")
            
    except Exception as e:
        print(f"⚠️ Error during RAG search: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run tests for common queries."""
    queries = [
        "What is Gravitas?",
        "Tell me about Gravitas Grounded Research",
        "What is the Gravitas system?",
        "Describe the architecture",
        "What is Qdrant?",
    ]
    
    for query in queries:
        await test_query(query)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
