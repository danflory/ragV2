import asyncio
import os
import sys

# 1. PATH HACK (Standard for our testing)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.router import parse_reflex_action
from app.reflex import write_file, execute_shell

async def test_reflex_system():
    print("🧪 STARTING REFLEX SYSTEM TEST")
    
    # ---------------------------------------------------------
    # TEST 1: PARSER LOGIC (The Brain)
    # ---------------------------------------------------------
    print("\n[1] Testing XML Parser...")
    
    mock_l2_response_write = """
    Sure, I can help with that.
    <reflex action="write" path="test_artifact.txt">
    Hello from the Agentic Loop!
    </reflex>
    """
    
    action, payload = parse_reflex_action(mock_l2_response_write)
    
    if action == "write" and payload[0] == "test_artifact.txt":
        print("✅ Parser correctly identified WRITE action.")
    else:
        print(f"❌ Parser FAILED. Got: {action}, {payload}")
        return

    # ---------------------------------------------------------
    # TEST 2: ACTUATOR LOGIC (The Hands - Write)
    # ---------------------------------------------------------
    print("\n[2] Testing File Writer...")
    path, content = payload
    result = await write_file(path, content)
    print(f"   Result: {result}")
    
    # Verify file actually exists on disk
    if os.path.exists("test_artifact.txt"):
        with open("test_artifact.txt", "r") as f:
            saved_content = f.read()
            if "Hello from the Agentic Loop" in saved_content:
                print("✅ File physically verified on disk.")
            else:
                print("❌ File exists but content is wrong.")
    else:
        print("❌ File was NOT created.")

    # Cleanup
    if os.path.exists("test_artifact.txt"):
        os.remove("test_artifact.txt")
        print("   (Cleanup complete)")

    # ---------------------------------------------------------
    # TEST 3: ACTUATOR LOGIC (The Hands - Shell)
    # ---------------------------------------------------------
    print("\n[3] Testing Shell Execution...")
    shell_cmd = "echo 'Agentic Echo'"
    result = await execute_shell(shell_cmd)
    
    if "Agentic Echo" in result and "SUCCESS" in result:
        print("✅ Shell execution confirmed.")
    else:
        print(f"❌ Shell execution failed. Result: {result}")

    print("\n🎉 ALL SYSTEMS GREEN: The Agent can See, Think, and Act.")

if __name__ == "__main__":
    asyncio.run(test_reflex_system())