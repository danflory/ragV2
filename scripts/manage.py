import asyncio
import sys
import httpx
import argparse

# Gravitas Management CLI
# Communicates via the API endpoints on port 5050

BASE_URL = "http://localhost:5050"

async def call_api(method, endpoint, json=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if method == "POST":
                resp = await client.post(url, json=json)
            elif method == "DELETE":
                resp = await client.delete(url)
            else:
                resp = await client.get(url)
            
            data = resp.json()
            if resp.status_code == 200 and data.get("status") == "success":
                print(f"✅ SUCCESS: {data.get('message', 'Operation complete')}")
            else:
                print(f"❌ FAILED: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

async def main():
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

    if args.command == "pull":
        print(f"📡 Requesting pull for {args.model}...")
        await call_api("POST", "/model/pull", {"model": args.model})
    elif args.command == "clear":
        print("🗑️ Requesting history clearance...")
        await call_api("DELETE", "/history")
    elif args.command == "ingest":
        print("🔍 Requesting document re-scan...")
        await call_api("POST", "/ingest")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
