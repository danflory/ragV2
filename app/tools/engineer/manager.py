#!/usr/bin/env python3
import asyncio
import sys
import httpx
import argparse
import os

# Ensure we can import app components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class GravitasManagerTool:
    """Tool for managing the Gravitas system via its API."""
    
    def __init__(self, base_url="http://localhost:5050"):
        self.base_url = base_url

    async def _call_api(self, method, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "POST":
                    resp = await client.post(url, json=json)
                elif method == "DELETE":
                    resp = await client.delete(url)
                else:
                    resp = await client.get(url)
                
                data = resp.json()
                if resp.status_code == 200 and data.get("status") == "success":
                    print(f"✅ SUCCESS: {data.get('message', 'Operation complete')}")
                    return True, data
                else:
                    print(f"❌ FAILED: {data.get('message', 'Unknown error')}")
                    return False, data
        except Exception as e:
            print(f"❌ CONNECTION ERROR: {e}")
            return False, str(e)

    async def execute(self, command, **kwargs):
        if command == "pull":
            model = kwargs.get("model")
            print(f"📡 Requesting pull for {model}...")
            return await self._call_api("POST", "/model/pull", {"model": model})
        elif command == "clear":
            print("🗑️ Requesting history clearance...")
            return await self._call_api("DELETE", "/history")
        elif command == "ingest":
            print("🔍 Requesting document re-scan...")
            return await self._call_api("POST", "/ingest")
        else:
            print(f"❌ Unknown command: {command}")
            return False, "Unknown command"

if __name__ == "__main__":
    tool = GravitasManagerTool()
    parser = argparse.ArgumentParser(description="Gravitas System Manager")
    subparsers = parser.add_subparsers(dest="command")

    # 1. Pull Model
    pull_parser = subparsers.add_parser("pull", help="Pull a new model into Ollama")
    pull_parser.add_argument("model", help="Model name (e.g., llama2, codellama:13b)")

    # 2. Clear History
    subparsers.add_parser("clear", help="Clear short-term chat history")

    # 3. Ingest
    subparsers.add_parser("ingest", help="Trigger document ingestion")

    args = parser.parse_args()

    if args.command:
        asyncio.run(tool.execute(args.command, **vars(args)))
    else:
        parser.print_help()
