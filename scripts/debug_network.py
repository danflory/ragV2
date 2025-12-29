import httpx
import asyncio
import os
from dotenv import load_dotenv

# Force load the .env to be absolutely sure
load_dotenv()

URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

async def main():
    print(f"🕵️ NETWORK DEBUG")
    print(f"--------------------------------------------------")
    print(f"Target URL: {URL}/api/tags")
    
    try:
        async with httpx.AsyncClient() as client:
            # Hit the API raw, just like curl
            response = await client.get(f"{URL}/api/tags")
            
            print(f"Status Code: {response.status_code}")
            print(f"Raw Response Text:\n{response.text}")
            
            data = response.json()
            models = data.get("models", [])
            print(f"--------------------------------------------------")
            print(f"✅ Parsed Model Count: {len(models)}")
            if len(models) > 0:
                print(f"Models Found: {[m.get('name') for m in models]}")
            else:
                print("❌ List is EMPTY (Split Brain verified)")

    except Exception as e:
        print(f"🔥 CONNECTION FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(main())