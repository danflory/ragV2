import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.container import container
from app.reflex import execute_git_sync

async def test_reflex_capability():
    print("🧠 Step 1: Testing L1 Intelligence (Does it know the code?)")
    # We ask L1 to trigger the action
    response = await container.l1_driver.generate("Please save the project and push to git.")
    
    print(f"   L1 Reply: [{response}]")
    
    if response == "<<GIT_SYNC>>":
        print("   ✅ L1 recognized the command!")
    else:
        print("   ❌ L1 missed the intent (Prompt tuning needed).")

    print("\n✋ Step 2: Testing Reflex Motor Function (Does the code work?)")
    # We force the action to ensure the permissions are right
    log = execute_git_sync("Test: Manual Reflex Check")
    print(f"   Reflex Log: {log}")

if __name__ == "__main__":
    asyncio.run(test_reflex_capability())