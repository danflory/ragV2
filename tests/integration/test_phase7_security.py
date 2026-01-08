import pytest
import httpx
import jwt
import time
import os
import uuid
from app.config import config

SUPERVISOR_URL = os.getenv("ROUTER_URL") or os.getenv("SUPERVISOR_URL") or os.getenv("L1_URL") or "http://localhost:8005"

# Secret matching the default in app.config
SECRET_KEY = config.JWT_SECRET_KEY

def generate_token(ghost_id: str, groups: list = None):
    payload = {
        "sub": ghost_id,
        "groups": groups or ["user"],
        "exp": time.time() + 3600
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.mark.asyncio
async def test_supervisor_health():
    """Verify service is running"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{SUPERVISOR_URL}/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_auth_missing_token():
    """Verify 401 when no token provided"""
    payload = {
        "model": "gemma2:27b",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SUPERVISOR_URL}/v1/chat/completions", json=payload)
        assert resp.status_code == 401
        assert "Missing Authorization header" in resp.text

@pytest.mark.asyncio
async def test_auth_invalid_token():
    """Verify 401 when token is garbage"""
    payload = {
        "model": "gemma2:27b",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    headers = {"Authorization": "Bearer not.a.valid.token"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SUPERVISOR_URL}/v1/chat/completions", json=payload, headers=headers)
        assert resp.status_code == 401

@pytest.mark.asyncio
async def test_auth_valid_token_allow():
    """Verify 200 (or execution error) when token is valid and allowed"""
    # Assuming "Supervisor_Managed_Agent" has default access to "gemma2:27b" (L1)
    token = generate_token("Supervisor_Managed_Agent", ["admin"])
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "model": "gemma2:27b",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{SUPERVISOR_URL}/v1/chat/completions", 
                json=payload, 
                headers=headers,
                timeout=5.0
            )
            # If Ollama is running, 200. If not, maybe 500.
            # If we hit Guardian Certification error (403), that means Auth & Policy PASSED.
            if resp.status_code == 403:
                error_detail = resp.json().get("detail", "")
                if "lacks a valid certificate" in error_detail:
                    # Success! We passed Auth and Policy, but failed purely on Guardian Cert logic
                    return
            
            if resp.status_code != 200:
                print(f"Execution result: {resp.status_code} - {resp.text}")
            
            assert resp.status_code in [200, 500, 400] 
            assert resp.status_code != 401
            # We already handled the specific 403 we allow check above
            if resp.status_code == 403:
                pytest.fail(f"Policy Rejection (Unexpected): {resp.text}")
            
        except httpx.ConnectError:
            pytest.fail("Supervisor is not reachable")

@pytest.mark.asyncio
async def test_policy_deny_resource():
    """Verify 403 when Policy Engine denies access"""
    # Create a token for a 'LimitedGuest' who shouldn't access L3
    token = generate_token("LimitedGuest", ["guest"])
    headers = {"Authorization": f"Bearer {token}"}
    
    # We need to ensure 'guest' group is restricted in access_policies.yaml
    # But since we can't easily change the file purely in test without mocking,
    # we test the GhostRegistry fallback.
    # If "LimitedGuest" is unknown and not Supervisor_Managed_Agent, it defaults to NO groups
    # or empty permissions unless mapped.
    
    payload = {
        "model": "gemini-1.5-pro", # L3 resource
        "messages": [{"role": "user", "content": "Analyze architecture"}]
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPERVISOR_URL}/v1/chat/completions",
            json=payload,
            headers=headers
        )
        assert resp.status_code == 403
        assert "Access denied" in resp.text
