"""
Advanced RAG Integration Tests
Tests complex queries that require synthesis across multiple files and deep understanding.
"""

import httpx
import asyncio

BASE_URL = "http://localhost:5050"
TIMEOUT = 60.0

async def test_query(question: str, expected_keywords: list):
    """Test a single RAG query and validate response quality."""
    print(f"\n{'='*80}")
    print(f"Q: {question}")
    print(f"{'='*80}")
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(f"{BASE_URL}/chat", json={"message": question})
        assert resp.status_code == 200
        data = resp.json()
        response = data["response"].lower()
        
        print(f"A: {data['response'][:500]}...")
        print(f"\nLayer: {data.get('layer', 'Unknown')}")
        
        # Check for expected keywords
        found = [kw for kw in expected_keywords if kw.lower() in response]
        missing = [kw for kw in expected_keywords if kw.lower() not in response]
        
        print(f"\n✅ Found keywords: {found}")
        if missing:
            print(f"⚠️  Missing keywords: {missing}")
        
        # Require at least 50% keyword match
        match_rate = len(found) / len(expected_keywords)
        assert match_rate >= 0.5, f"Only {match_rate*100:.0f}% keyword match"
        
        return data["response"]

async def main():
    tests = [
        {
            "question": "How does the Librarian's Night Shift differ from the standard Ingestor, and which produces better semantic search results?",
            "keywords": ["summary", "AI", "semantic", "chunk", "quality", "librarian", "ingestor"]
        },
        {
            "question": "What is the complete flow from when a user sends a chat message until they receive a response, including all the layers and components involved?",
            "keywords": ["route", "L1", "RAG", "context", "generate", "escalate", "response"]
        },
        {
            "question": "Explain how VRAM is allocated across the two GPUs and what happens during a mode switch from DEV to RAG.",
            "keywords": ["Titan", "1060", "generation", "embedding", "load", "model", "switch"]
        },
        {
            "question": "If I wanted to add a new reflex action type (like 'sql_query'), what files would I need to modify and what would the implementation look like?",
            "keywords": ["router", "parse", "reflex", "action", "regex", "execute"]
        },
        {
            "question": "What's the relationship between MinIO, Qdrant, and the vector embeddings? Walk me through how a document becomes searchable.",
            "keywords": ["blob", "storage", "vector", "embedding", "index", "search", "payload"]
        },
        {
            "question": "How does the telemetry system track VRAM usage and what happens if we hit the 2GB free threshold?",
            "keywords": ["telemetry", "VRAM", "check", "overload", "lockout", "threshold"]
        }
    ]
    
    print("\n🚀 ADVANCED RAG INTEGRATION TESTS")
    print("Testing improved RAG quality with Librarian AI summaries\n")
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}/{len(tests)}")
        try:
            await test_query(test["question"], test["keywords"])
            passed += 1
            print("✅ PASSED")
        except AssertionError as e:
            failed += 1
            print(f"❌ FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"⚠️  ERROR: {e}")
        
        # Small delay between tests
        await asyncio.sleep(2)
    
    print(f"\n{'='*80}")
    print(f"RESULTS: {passed}/{len(tests)} passed, {failed}/{len(tests)} failed")
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(main())
