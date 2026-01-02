import subprocess
import json
import sys

# The exact command Cline is trying to run
cmd = [
    "docker", "exec", "-i", 
    "gravitas_mcp", 
    "python3", "-u", "-m", "app.mcp_server", "--stdio"
]

print(f"Testing Command: {' '.join(cmd)}")
print("Sending JSON-RPC Initialize Request...")

try:
    # Open the connection
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr, # let us see errors on screen
        text=True
    )

    # JSON-RPC Handshake Message
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-script", "version": "1.0"}
        },
        "id": 1
    }

    # Send request into the container
    json_str = json.dumps(init_request) + "\n"
    process.stdin.write(json_str)
    process.stdin.flush()

    # Read the response
    response = process.stdout.readline()
    
    if response:
        print("\n✅ SUCCESS! Received Response:")
        print(json.loads(response))
    else:
        print("\n❌ FAILURE: No data received. (Check docker logs)")

    process.terminate()

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    