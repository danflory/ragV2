import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.reflex import execute_git_sync

async def test_git_push_behavior():
    print("🚀 Triggering Git Sync...")
    
    # We expect this to fail on the 'push' step inside the container
    result = await execute_git_sync("Headless Test Sync")
    
    print("\n--- RESULT ---")
    print(result)
    
    if "GIT ERROR" in result and "could not read Username" in result:
        print("\n✅ REPRODUCTION SUCCESSFUL: Caught expected Auth error.")
    elif "GIT SYNC COMPLETE" in result:
        print("\n❓ UNEXPECTED SUCCESS: Git push worked?")
    else:
        print("\n⚠️ UNKNOWN STATE.")

if __name__ == "__main__":
    asyncio.run(test_git_push_behavior())
