"""
RAG Diagnostic Tests

This test suite performs deeper diagnostics on the RAG system to understand
why certain queries may not be retrieving the expected context.
"""

import httpx
import pytest
import asyncio

BASE_URL = "http://localhost:5050"
TIMEOUT = 30.0


class TestRAGRetrieval:
    """Test RAG retrieval quality and context injection."""
    
    @pytest.mark.asyncio
    async def test_what_is_gravitas_verbose(self):
        """Detailed test for 'What is Gravitas' query to see what's happening."""
        query = "What is Gravitas?"
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": query}
            )
            assert resp.status_code == 200
            data = resp.json()
            
            print("\n" + "="*60)
            print(f"Query: {query}")
            print("="*60)
            print(f"Response Layer: {data['layer']}")
            print(f"Response Length: {len(data['response'])} chars")
            print("-"*60)
            print("FULL RESPONSE:")
            print(data['response'])
            print("="*60)
            
            # Check for keywords that should appear
            response_lower = data['response'].lower()
            
            keywords = {
                "rag": "Retrieval Augmented Generation",
                "dual-gpu": "Dual GPU architecture",
                "qdrant": "Vector database",
                "grounded": "Grounded research philosophy",
                "titan": "Hardware description",
                "minio": "Storage backend",
                "l1": "Layer 1 model",
                "research": "Research capability"
            }
            
            found_keywords = []
            missing_keywords = []
            
            for keyword, description in keywords.items():
                if keyword in response_lower:
                    found_keywords.append(f"✅ {keyword} ({description})")
                else:
                    missing_keywords.append(f"❌ {keyword} ({description})")
            
            print("\nKEYWORD ANALYSIS:")
            for k in found_keywords:
                print(k)
            for k in missing_keywords:
                print(k)
            
            print(f"\nScore: {len(found_keywords)}/{len(keywords)} keywords found")
    
    @pytest.mark.asyncio
    async def test_alternative_gravitas_queries(self):
        """Test various ways of asking about Gravitas."""
        queries = [
            "Describe the Gravitas system",
            "Tell me about Gravitas Grounded Research",
            "What is the Gravitas RAG platform?",
            "Explain the Gravitas architecture",
            "What does Gravitas do?"
        ]
        
        for query in queries:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.post(
                    f"{BASE_URL}/chat",
                    json={"message": query}
                )
                assert resp.status_code == 200
                data = resp.json()
                
                response_lower = data['response'].lower()
                
                # Count how many Gravitas-specific terms appear
                gravitas_terms = ['rag', 'grounded', 'qdrant', 'dual-gpu', 'minio', 'vector']
                term_count = sum(1 for term in gravitas_terms if term in response_lower)
                
                print(f"\n{'='*60}")
                print(f"Query: {query}")
                print(f"Terms found: {term_count}/{len(gravitas_terms)}")
                print(f"First 200 chars: {data['response'][:200]}...")
    
    @pytest.mark.asyncio
    async def test_specific_component_queries(self):
        """Test queries about specific components to verify RAG is working."""
        test_cases = [
            {
                "query": "What is Qdrant used for in Gravitas?",
                "expected_keywords": ["vector", "hybrid", "search", "memory"]
            },
            {
                "query": "What is MinIO in Gravitas?",
                "expected_keywords": ["storage", "blob", "object", "minio"]
            },
            {
                "query": "What is the Titan RTX GPU used for?",
                "expected_keywords": ["generation", "l1", "inference", "24gb"]
            },
            {
                "query": "What models run on GPU 1?",
                "expected_keywords": ["embedding", "1060", "6gb"]
            }
        ]
        
        results = []
        for test_case in test_cases:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.post(
                    f"{BASE_URL}/chat",
                    json={"message": test_case["query"]}
                )
                assert resp.status_code == 200
                data = resp.json()
                
                response_lower = data['response'].lower()
                keywords_found = [
                    kw for kw in test_case["expected_keywords"] 
                    if kw in response_lower
                ]
                
                success = len(keywords_found) > 0
                results.append({
                    "query": test_case["query"],
                    "success": success,
                    "keywords_found": keywords_found,
                    "total_keywords": len(test_case["expected_keywords"])
                })
        
        print("\n" + "="*60)
        print("COMPONENT QUERY RESULTS")
        print("="*60)
        for r in results:
            status = "✅ PASS" if r["success"] else "❌ FAIL"
            print(f"\n{status}: {r['query']}")
            print(f"  Found {len(r['keywords_found'])}/{r['total_keywords']} keywords: {', '.join(r['keywords_found'])}")
        
        # Assert that at least 75% of queries succeeded
        success_rate = sum(1 for r in results if r["success"]) / len(results)
        assert success_rate >= 0.75, f"Success rate {success_rate:.1%} is below 75%"
    
    @pytest.mark.asyncio
    async def test_generic_vs_context_aware(self):
        """
        Test to distinguish between generic AI responses and context-aware responses.
        Generic responses indicate RAG context is not being used.
        """
        test_cases = [
            {
                "query": "What is the Journal Rule?",
                "generic_phrases": [
                    "i don't have specific information",
                    "i'm not aware",
                    "i don't know",
                    "in general",
                    "typically"
                ],
                "context_phrases": [
                    "journal",
                    "documentation",
                    "gravitas",
                    "decision"
                ]
            },
            {
                "query": "How do I run tests?",
                "generic_phrases": [
                    "generally",
                    "typically",
                    "usually you would"
                ],
                "context_phrases": [
                    "pytest",
                    "tests/",
                    "gravitas"
                ]
            }
        ]
        
        for test_case in test_cases:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.post(
                    f"{BASE_URL}/chat",
                    json={"message": test_case["query"]}
                )
                assert resp.status_code == 200
                data = resp.json()
                
                response_lower = data['response'].lower()
                
                generic_count = sum(
                    1 for phrase in test_case["generic_phrases"]
                    if phrase in response_lower
                )
                context_count = sum(
                    1 for phrase in test_case["context_phrases"]
                    if phrase in response_lower
                )
                
                is_context_aware = context_count > generic_count
                
                print(f"\n{'='*60}")
                print(f"Query: {test_case['query']}")
                print(f"Generic phrases: {generic_count}")
                print(f"Context phrases: {context_count}")
                print(f"Result: {'✅ Context-aware' if is_context_aware else '❌ Generic'}")
                
                assert is_context_aware, f"Response appears generic for: {test_case['query']}"


if __name__ == "__main__":
    async def run_diagnostics():
        print("🔍 Running RAG Diagnostic Tests...\n")
        
        test_suite = TestRAGRetrieval()
        
        tests = [
            ("Verbose 'What is Gravitas' Test", test_suite.test_what_is_gravitas_verbose),
            ("Alternative Query Formats", test_suite.test_alternative_gravitas_queries),
            ("Component-Specific Queries", test_suite.test_specific_component_queries),
            ("Generic vs Context-Aware", test_suite.test_generic_vs_context_aware),
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'#'*60}")
            print(f"# {test_name}")
            print(f"{'#'*60}")
            try:
                await test_func()
                print(f"\n✅ {test_name} COMPLETED")
            except AssertionError as e:
                print(f"\n❌ {test_name} FAILED: {e}")
            except Exception as e:
                print(f"\n⚠️ {test_name} ERROR: {e}")
                import traceback
                traceback.print_exc()
    
    asyncio.run(run_diagnostics())
