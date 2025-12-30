import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.container import container

async def test_google():
    print("🚀 Testing L3 (Google Gemini)...")
    driver = container.get_l3_driver()
    
    print(f"   Model: {driver.model_name}")
    print(f"   Key Present: {'✅' if driver.api_key else '❌'}")
    
    response = await driver.generate("Explain the difference between L1, L2, and L3 cache in a CPU.")
    
    print("\n💡 Gemini Response:")
    print("-" * 40)
    print(response[:500] + "...") # Print first 500 chars
    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_google())