"""
Integrated RAG Prompt Tests

This test suite validates that the Gravitas RAG system correctly handles
expected user prompts and returns meaningful results based on the indexed
documentation and codebase.

Test Categories:
1. Architecture Questions - Queries about system design
2. Hardware Questions - Queries about GPU and resource allocation
3. Development Workflow - Questions about testing, protocols, and TDD
4. Feature Queries - Questions about specific capabilities
5. Troubleshooting - Questions about debugging and recovery
"""

import httpx
import pytest
import asyncio
import time

BASE_URL = "http://localhost:5050"
TIMEOUT = 30.0  # Allow time for model inference


class TestArchitectureQueries:
    """Test queries about system architecture and design."""
    
    @pytest.mark.asyncio
    async def test_what_is_gravitas(self):
        """User asks: What is Gravitas?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is Gravitas?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "response" in data
            response_text = data["response"].lower()
            
            # Should mention RAG, research, or grounded
            assert any(keyword in response_text for keyword in [
                "rag", "research", "grounded", "dual-gpu", "vector"
            ]), f"Response doesn't describe Gravitas: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_three_layer_brain(self):
        """User asks: What is the 3-layer brain architecture?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "Explain the 3-layer brain architecture"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention L1, L2, L3 or layers
            assert any(keyword in response_text for keyword in [
                "l1", "l2", "l3", "layer", "reflex", "reason", "research"
            ]), f"Response doesn't explain layers: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_memory_storage(self):
        """User asks: How does Gravitas store memory?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "How does Gravitas store memory?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention Qdrant, MinIO, or vector storage
            assert any(keyword in response_text for keyword in [
                "qdrant", "minio", "vector", "hybrid", "storage"
            ]), f"Response doesn't describe storage: {data['response']}"


class TestHardwareQueries:
    """Test queries about hardware and GPU configuration."""
    
    @pytest.mark.asyncio
    async def test_gpu_allocation(self):
        """User asks: What GPUs does Gravitas use?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What GPUs does Gravitas use?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention Titan RTX or GTX 1060
            assert any(keyword in response_text for keyword in [
                "titan", "1060", "gpu", "dual", "24gb", "6gb"
            ]), f"Response doesn't describe GPUs: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_vram_usage(self):
        """User asks: How is VRAM allocated?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "How is VRAM allocated in Gravitas?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention generation, embeddings, or separation
            assert any(keyword in response_text for keyword in [
                "vram", "generation", "embedding", "titan", "1060"
            ]), f"Response doesn't explain VRAM: {data['response']}"


class TestDevelopmentWorkflow:
    """Test queries about development protocols and testing."""
    
    @pytest.mark.asyncio
    async def test_tdd_approach(self):
        """User asks: Does Gravitas follow TDD?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "Does Gravitas follow TDD?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention test-driven development or testing
            assert any(keyword in response_text for keyword in [
                "tdd", "test", "pytest", "red-green-refactor"
            ]), f"Response doesn't mention TDD: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_run_tests(self):
        """User asks: How do I run the test suite?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "How do I run the test suite?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention pytest or test command
            assert any(keyword in response_text for keyword in [
                "pytest", "test", "tests/", "python"
            ]), f"Response doesn't explain testing: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_journal_rule(self):
        """User asks: What is the Journal Rule?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is the Journal Rule?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention documentation or journal
            assert any(keyword in response_text for keyword in [
                "journal", "documentation", "decision", "docs"
            ]), f"Response doesn't explain journal rule: {data['response']}"


class TestFeatureQueries:
    """Test queries about specific features and capabilities."""
    
    @pytest.mark.asyncio
    async def test_nexus_dashboard(self):
        """User asks: What is the Nexus Dashboard?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is the Nexus Dashboard?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention UI, dashboard, or web interface
            assert any(keyword in response_text for keyword in [
                "dashboard", "ui", "web", "interface", "nexus"
            ]), f"Response doesn't describe Nexus: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_rag_mode(self):
        """User asks: What is RAG mode?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is RAG mode?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention retrieval, research, or knowledge
            assert any(keyword in response_text for keyword in [
                "rag", "retrieval", "research", "knowledge", "document"
            ]), f"Response doesn't explain RAG mode: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_gatekeeper(self):
        """User asks: What is the Gatekeeper?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is the Gatekeeper?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention safety, security, or validation
            assert any(keyword in response_text for keyword in [
                "safety", "security", "gatekeeper", "validation", "command"
            ]), f"Response doesn't explain Gatekeeper: {data['response']}"


class TestTroubleshootingQueries:
    """Test queries about troubleshooting and system recovery."""
    
    @pytest.mark.asyncio
    async def test_system_recovery(self):
        """User asks: How do I reset the system?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "How do I reset the Gravitas system?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention reset script or recovery
            assert any(keyword in response_text for keyword in [
                "reset", "script", "recovery", "docker", "restart"
            ]), f"Response doesn't explain reset: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_check_health(self):
        """User asks: How do I check system health?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "How do I check Gravitas health?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention health, monitor, or status
            assert any(keyword in response_text for keyword in [
                "health", "monitor", "status", "nvidia-smi", "docker"
            ]), f"Response doesn't explain health check: {data['response']}"


class TestRoadmapQueries:
    """Test queries about the project roadmap and future features."""
    
    @pytest.mark.asyncio
    async def test_current_phase(self):
        """User asks: What is the current development phase?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is the current development phase of Gravitas?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention phase or version
            assert any(keyword in response_text for keyword in [
                "phase", "version", "4.2", "roadmap"
            ]), f"Response doesn't describe current phase: {data['response']}"
    
    @pytest.mark.asyncio
    async def test_upcoming_features(self):
        """User asks: What features are planned?"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What features are planned for future phases?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            response_text = data["response"].lower()
            
            # Should mention upcoming features or phases
            assert any(keyword in response_text for keyword in [
                "phase", "future", "planned", "upcoming", "telemetry", "supervisor"
            ]), f"Response doesn't describe upcoming features: {data['response']}"


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.mark.asyncio
    async def test_empty_message(self):
        """User sends empty message."""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": ""}
            )
            # Should still return 200 but might have minimal response
            assert resp.status_code == 200
            data = resp.json()
            assert "response" in data
    
    @pytest.mark.asyncio
    async def test_very_long_query(self):
        """User sends very long query to test context handling."""
        long_query = "Tell me about " + "the architecture and design " * 50
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": long_query}
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "response" in data
    
    @pytest.mark.asyncio
    async def test_unrelated_query(self):
        """User asks question unrelated to Gravitas."""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{BASE_URL}/chat",
                json={"message": "What is the capital of France?"}
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "response" in data
            # System might not have context, but should still respond


# Manual execution helper
if __name__ == "__main__":
    import sys
    
    async def run_single_test(test_name: str):
        """Run a single test by name for debugging."""
        print(f"\n{'='*60}")
        print(f"Running Test: {test_name}")
        print(f"{'='*60}\n")
        
        # Map test names to test classes and methods
        test_map = {
            "what_is_gravitas": TestArchitectureQueries().test_what_is_gravitas,
            "three_layer": TestArchitectureQueries().test_three_layer_brain,
            "memory_storage": TestArchitectureQueries().test_memory_storage,
            "gpu_allocation": TestHardwareQueries().test_gpu_allocation,
            "vram": TestHardwareQueries().test_vram_usage,
            "tdd": TestDevelopmentWorkflow().test_tdd_approach,
            "run_tests": TestDevelopmentWorkflow().test_run_tests,
            "journal": TestDevelopmentWorkflow().test_journal_rule,
            "nexus": TestFeatureQueries().test_nexus_dashboard,
            "rag_mode": TestFeatureQueries().test_rag_mode,
            "gatekeeper": TestFeatureQueries().test_gatekeeper,
            "reset": TestTroubleshootingQueries().test_system_recovery,
            "health": TestTroubleshootingQueries().test_check_health,
            "current_phase": TestRoadmapQueries().test_current_phase,
            "upcoming": TestRoadmapQueries().test_upcoming_features,
        }
        
        if test_name in test_map:
            try:
                await test_map[test_name]()
                print(f"\n✅ Test '{test_name}' PASSED")
            except AssertionError as e:
                print(f"\n❌ Test '{test_name}' FAILED")
                print(f"Reason: {e}")
                return False
            except Exception as e:
                print(f"\n⚠️ Test '{test_name}' ERROR")
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print(f"❌ Unknown test: {test_name}")
            print(f"\nAvailable tests: {', '.join(test_map.keys())}")
            return False
        
        return True
    
    async def run_all_tests():
        """Run all tests sequentially with detailed output."""
        test_classes = [
            ("Architecture Queries", TestArchitectureQueries()),
            ("Hardware Queries", TestHardwareQueries()),
            ("Development Workflow", TestDevelopmentWorkflow()),
            ("Feature Queries", TestFeatureQueries()),
            ("Troubleshooting", TestTroubleshootingQueries()),
            ("Roadmap Queries", TestRoadmapQueries()),
        ]
        
        results = {"passed": 0, "failed": 0, "errors": 0}
        failed_tests = []
        
        for category_name, test_class in test_classes:
            print(f"\n{'='*60}")
            print(f"Category: {category_name}")
            print(f"{'='*60}")
            
            # Get all test methods
            test_methods = [
                method for method in dir(test_class)
                if method.startswith("test_") and callable(getattr(test_class, method))
            ]
            
            for method_name in test_methods:
                test_method = getattr(test_class, method_name)
                test_display_name = method_name.replace("test_", "").replace("_", " ").title()
                
                print(f"\n▶ Running: {test_display_name}...")
                
                try:
                    await test_method()
                    print(f"  ✅ PASSED")
                    results["passed"] += 1
                except AssertionError as e:
                    print(f"  ❌ FAILED: {e}")
                    results["failed"] += 1
                    failed_tests.append((category_name, test_display_name, str(e)))
                except Exception as e:
                    print(f"  ⚠️ ERROR: {e}")
                    results["errors"] += 1
                    failed_tests.append((category_name, test_display_name, f"ERROR: {e}"))
                
                # Small delay between tests
                await asyncio.sleep(0.5)
        
        # Final summary
        print(f"\n{'='*60}")
        print("FINAL RESULTS")
        print(f"{'='*60}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⚠️ Errors: {results['errors']}")
        print(f"Total: {sum(results.values())}")
        
        if failed_tests:
            print(f"\n{'='*60}")
            print("FAILED TESTS SUMMARY")
            print(f"{'='*60}")
            for category, test, reason in failed_tests:
                print(f"\n[{category}] {test}")
                print(f"  Reason: {reason}")
    
    # Check if specific test requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        asyncio.run(run_single_test(test_name))
    else:
        print("🚀 Running All Integrated RAG Prompt Tests...")
        asyncio.run(run_all_tests())
