import os
import sys
import asyncio
import httpx
from google import genai
from dotenv import load_dotenv

# Load environment variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import config

async def check_openai():
    print("\n🔎 Checking OpenAI Models...")
    headers = {"Authorization": f"Bearer {config.L2_KEY}"}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.openai.com/v1/models", headers=headers)
            if resp.status_code == 200:
                data = resp.json()['data']
                # Filter for "gpt" models and sort them
                gpt_models = sorted([m['id'] for m in data if 'gpt' in m['id']])
                print(f"✅ OpenAI Success! Found {len(gpt_models)} models.")
                print("--- VALID MODEL IDs ---")
                for m in gpt_models:
                    # Only print relevant chat models to keep it clean
                    if "4o" in m or "mini" in m or "5" in m:
                        print(f" • {m}")
            else:
                print(f"❌ OpenAI Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ OpenAI Connection Failed: {e}")

async def check_google():
    print("\n🔎 Checking Google Gemini Models...")
    try:
        client = genai.Client(api_key=config.L3_KEY)
        # Fetch list of models
        pager = client.models.list()
        print("✅ Google Success!")
        print("--- VALID MODEL IDs ---")
        for m in pager:
            # We only care about generative models
            if "gemini" in m.name and "vision" not in m.name:
                # The API returns 'models/gemini-1.5-pro', we usually just need the part after 'models/'
                print(f" • {m.name.replace('models/', '')}")
    except Exception as e:
        print(f"❌ Google Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_openai())
    asyncio.run(check_google())