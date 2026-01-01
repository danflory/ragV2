import sys
import os
import httpx
import asyncio

# Testing the end-to-end sync trigger
async def test_sync_trigger():
    print("🧪 PROBE: Testing End-to-End Sync Trigger...")
    
    url = "http://localhost:5050/chat"
    payload = {"message": "save the code please"}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"   -> Sending message: {payload['message']}")
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ RESPONSE RECEIVED:")
                print(f"      {data['response']}")
                
                if "Git Sync Triggered" in data['response']:
                    print("🎉 SUCCESS: Protocol and Sync Verified.")
                else:
                    print("⚠️ WARNING: Sync message not found in response. Did L1 trigger it?")
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                print(response.text)
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_sync_trigger())
