import pytest
import httpx
import os
import jwt
import time
from app.config import config

GATEKEEPER_URL = os.getenv("GATEKEEPER_URL", "http://gravitas_gatekeeper:8001")
SECRET_KEY = config.JWT_SECRET_KEY

def generate_token(ghost_id: str, groups: list = None):
    payload = {
        "sub": ghost_id,
        "groups": groups or ["user"],
        "exp": time.time() + 3600
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.mark.asyncio
async def test_gatekeeper_health():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{GATEKEEPER_URL}/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_gatekeeper_validate_allow():
    token = generate_token("Supervisor_Managed_Agent", ["admin"])
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "action": "execute",
        "resource": "gemma2:27b",
        "metadata": {"test": "true"}
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{GATEKEEPER_URL}/validate", json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["allowed"] is True
        assert data["ghost_id"] == "Supervisor_Managed_Agent"

@pytest.mark.asyncio
async def test_gatekeeper_validate_deny():
    # Limited guest accessing admin resource
    token = generate_token("LimitedGuest", ["guest"])
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "action": "execute",
        "resource": "gemini-3-pro-preview", # Protected resource
        "metadata": {"test": "true"}
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{GATEKEEPER_URL}/validate", json=payload, headers=headers)
        assert resp.status_code == 403
        data = resp.json()
        assert "Access denied" in data["detail"]
