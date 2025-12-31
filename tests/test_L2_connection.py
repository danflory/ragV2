import asyncio
import os
import sys

# 1. PATH HACK: Force Python to see the 'app' folder from the 'tests' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import config
from app.L2_network import DeepInfraDriver

async def test_deepinfra():
    print(f"🔌 Testing Connection to: {config.L2_URL}")
    # Mask key for safety in logs
    masked_key = f"{config.L2_KEY[:4]}...{config.L2_KEY[-4:]}" if config.L2_KEY else "NONE"
    print(f"🔑 Using Key: {masked_key}")
    
    # 2. Instantiate the Driver
    driver = DeepInfraDriver(
        api_key=config.L2_KEY,
        base_url=config.L2_URL,
        model=config.L2_MODEL
    )
    
    # 3. Health Check
    if not await driver.check_health():
        print("❌ Health Check Failed: Key is missing.")
        return

    # 4. Live Fire Test
    print("📨 Sending prompt: 'What is the speed of light?'")
    try:
        response = await driver.generate("What is the speed of light?")
        print(f"\n✅ SUCCESS! Response received:\n{'-'*40}\n{response}\n{'-'*40}")
    except Exception as e:
        print(f"\n❌ CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(test_deepinfra())