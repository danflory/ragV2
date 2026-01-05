#!/usr/bin/env python3
"""
Direct test of RAG retrieval within the container
"""
import asyncio
import os

os.environ["QDRANT_HOST"] = "Gravitas_qdrant"
os.environ["MINIO_ENDPOINT"] = "Gravitas_minio:9000"

async def main():
    from app.container import container
    
    print("=" * 80)
    print("DIRECT RAG RETRIEVAL TEST")
    print("=" * 80)
    
    query = "What are the phases in the Gravitas roadmap?"
    print(f"\nQuery: {query}\n")
    
    # Test RAG search
    results = await container.memory.search(query, top_k=5)
    
    print(f"✅ Retrieved {len(results)} chunks\n")
    
    for i, chunk in enumerate(results, 1):
        print(f"--- Chunk {i} ---")
        print(chunk[:400])
        print()
    
    # Now test with L1 model
    print("=" * 80)
    print("TESTING L1 GENERATION WITH RAG CONTEXT")
    print("=" * 80)
    
    # Build context
    context_hint = "--- KNOWLEDGE BASE ---\n" + "\n\n".join(results) + "\n\n"
    full_prompt = f"{context_hint}User: {query}"
    
    print(f"\nSending to L1 model ({container.l1_driver.model_name})...\n")
    
    response = await container.l1_driver.generate(full_prompt)
    
    print("=" * 80)
    print("L1 RESPONSE")
    print("=" * 80)
    print(response)
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
