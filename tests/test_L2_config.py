import sys
import os
import asyncio

# Path hack
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.container import container

async def verify_l2_wiring():
    print("📋 Verifying L2 Configuration Wiring...")
    
    driver = container.get_l2_driver()
    
    print(f"   Driver Class: {driver.__class__.__name__}")
    print(f"   Target Model: {driver.model_name}")
    print(f"   Target URL:   {driver.base_url}")
    print(f"   API Key Set?  {'✅ Yes' if driver.api_key else '❌ No (Check .env)'}")

    if driver.api_key:
        print("\n🚀 Attempting Live Connection...")
        response = await driver.generate("Print the word 'Connection' and nothing else.")
        print(f"   Result: {response}")
    else:
        print("\n⚠️  Skipping live test (No Key). Config structure verified.")

if __name__ == "__main__":
    asyncio.run(verify_l2_wiring())