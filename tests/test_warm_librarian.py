import httpx
import asyncio
import time
import pytest
import os

BASE_URL = "http://localhost:5050"
TIMEOUT = 300.0  # Long timeout for model loading

async def get_gpu_usage():
    """Fetches VRAM usage from the health endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/health/detailed")
        if resp.status_code == 200:
            data = resp.json()
            return data["health"]["gpu"]["used"]
    return 0

async def monitor_load():
    """Polls until VRAM usage indicates gemma2:27b is loaded."""
    print("\n📡 Monitoring VRAM for Model Load (Gemma 27b)...")
    
    # Gemma 27B is ~15GB. We look for a jump above 12GB used on the primary GPU.
    # Note: health/detailed currently only reports the first GPU in its summary dict.
    
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        used = await get_gpu_usage()
        print(f"📊 Current VRAM: {used} MB")
        
        if used > 12000:
            print(f"✅ Model appears LOADED ({used} MB)")
            return True
        
        await asyncio.sleep(5)
    
    print("❌ Timeout waiting for model load.")
    return False

@pytest.mark.asyncio
async def test_librarian_with_warmup():
    """
    1. Preload the model (Switch to RAG Mode).
    2. Wait 60 seconds (User requested timeout).
    3. Run Night Shift (Librarian).
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # 1. PRELOAD / MODE SWITCH
        print("\n🚀 PRELOADING MODEL (Switching to RAG Mode - this might take 1-2 mins)...")
        # Increasing timeout for this specific call to 300s
        resp = await client.post(f"{BASE_URL}/system/mode", json={"mode": "rag"}, timeout=300.0)
        assert resp.status_code == 200
        print("✅ Mode switch command accepted by server.")
        
        # 2. RUN TIMEOUT (60 Seconds)
        print("⏳ WAITING 60 SECONDS (User requested stabilization wait)...")
        for i in range(60, 0, -10):
            print(f"   {i} seconds remaining...")
            await asyncio.sleep(10)
            
        # 3. RUN NIGHT SHIFT
        print("🧹 TRIGGERING NIGHT SHIFT (Librarian)...")
        start_proc = time.time()
        resp = await client.post(f"{BASE_URL}/agents/librarian/run", timeout=300.0)
        duration = time.time() - start_proc
        
        assert resp.status_code == 200
        data = resp.json()
        if data["status"] == "success":
            print(f"✅ Librarian finished in {duration:.2f}s")
            print(f"📁 Files processed: {data['files_processed']}")
        else:
            print(f"❌ Librarian failed: {data.get('message')}")
            assert False
        
if __name__ == "__main__":
    asyncio.run(test_librarian_with_warmup())
