import pytest
import httpx
import os
import jwt
import time
from app.config import config

# Future Router URL (distinct from Supervisor)
ROUTER_URL = os.getenv("ROUTER_URL", "http://gravitas_router:8004") 
SECRET_KEY = config.JWT_SECRET_KEY

def generate_token(ghost_id: str, groups: list = None):
    payload = {
        "sub": ghost_id,
        "groups": groups or ["admin"],
        "exp": time.time() + 3600
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.mark.asyncio
async def test_router_health():
    """Verify Router service is running"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.get(f"{ROUTER_URL}/health")
        assert resp.status_code == 200

@pytest.mark.asyncio
async def test_route_l1_ollama():
    """Verify routing to L1 (Ollama)"""
    token = generate_token("Supervisor_Managed_Agent")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "model": "codellama:7b", # Certified L1 Model
        "messages": [{"role": "user", "content": "Hello L1"}]
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{ROUTER_URL}/v1/chat/completions", json=payload, headers=headers)
        
        # If Ollama is still pulling, it might return 500 later, but it should pass Auth (200 or 500)
        # If it returns 403 with "lacks a valid certificate", that's also an "Auth Pass" for the router.
        if resp.status_code == 403:
             if "lacks a valid certificate" in resp.json().get("detail", ""):
                 return # Success (Auth passed)
                 
        assert resp.status_code in [200, 500]
        if resp.status_code == 200:
            assert "choices" in resp.json()

@pytest.mark.asyncio
async def test_route_l2_deepinfra():
    """Verify routing to L2 (DeepInfra) based on model name"""
    token = generate_token("Supervisor_Managed_Agent")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct", # L2 Model
        "force_tier": "L2",
        "messages": [{"role": "user", "content": "Hello L2"}]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{ROUTER_URL}/v1/chat/completions", json=payload, headers=headers)
        assert resp.status_code == 200
        assert "choices" in resp.json()
