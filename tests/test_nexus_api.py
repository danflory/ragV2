import httpx
import pytest
import asyncio

BASE_URL = "http://localhost:5050"

@pytest.mark.asyncio
async def test_health_detailed():
    """Verifies the detailed health endpoint returns the correct structure.
    Note: With dual-GPU setup, we now have ollama (generation) and ollama_embed (embeddings)
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{BASE_URL}/health/detailed")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "health" in data
        assert "ollama" in data["health"]  # GPU 0 - Generation
        assert "ollama_embed" in data["health"] # GPU 1 - Embeddings
        assert "postgres" in data["health"]

@pytest.mark.asyncio
async def test_stats_summary():
    """Verifies the stats summary provides numeric data."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{BASE_URL}/stats/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "summary" in data
        assert "total_requests" in data["summary"]
        assert isinstance(data["summary"]["total_requests"], int)

@pytest.mark.asyncio
async def test_cors_headers():
    """Verifies that CORS headers are present for the dashboard."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        # FastAPI CORS requires Origin header to be present to return Access-Control-Allow-Origin
        headers = {"Origin": "http://localhost:8080"}
        resp = await client.options(f"{BASE_URL}/chat", headers=headers)
        assert "access-control-allow-origin" in resp.headers
        assert resp.headers["access-control-allow-origin"] == "*"

@pytest.mark.asyncio
async def test_model_pull_endpoint():
    """Verifies the pull endpoint initiates correctly."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        # We test with a dummy model or one we have to ensure it non-blocks
        resp = await client.post(f"{BASE_URL}/model/pull", json={"model": "codellama:7b"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

if __name__ == "__main__":
    # If running manually without pytest
    async def run_all():
        print("🚀 Starting Headless API Tests...")
        try:
            await test_health_detailed()
            print("✅ Health Detailed: PASSED")
            await test_stats_summary()
            print("✅ Stats Summary: PASSED")
            await test_cors_headers()
            print("✅ CORS Headers: PASSED")
            print("\n💯 ALL API TESTS SUCCESSFUL.")
        except Exception as e:
            import traceback
            print(f"❌ TEST FAILED: {e}")
            traceback.print_exc()
            
    asyncio.run(run_all())
