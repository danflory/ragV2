
import asyncio
import httpx
import sys

# Configuration
GPU0_URL = "http://localhost:11434"
GPU1_URL = "http://localhost:11435"

# Expected Model Matrix
# Format: { Url: { "required": [models], "forbidden": [models] } }
EXPECTED_MATRIX = {
    GPU0_URL: { 
        "name": "GPU 0 (Titan RTX)",
        "required": ["gemma2:27b"], # Night Shift / RAG
        # "forbidden": ["codellama:7b"] # We might allow it as fallback, but ideally it's on GPU 1
    },
    GPU1_URL: {
        "name": "GPU 1 (GTX 1060)",
        "required": ["codellama:7b", "nomic-embed-text:latest"], # Miner & Embeddings
        "forbidden": ["gemma2:27b"] # Too big
    }
}

async def check_instance(url, config):
    name = config["name"]
    print(f"\n--- Checking {name} ({url}) ---")
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. List Tags
            resp = await client.get(f"{url}/api/tags")
            if resp.status_code != 200:
                print(f"❌ Failed to reach {name}: {resp.status_code}")
                return False
            
            models = resp.json().get("models", [])
            installed_names = [m['name'] for m in models]
            
            # Check Required
            all_good = True
            for req in config.get("required", []):
                if req not in installed_names:
                    print(f"   ❌ MISSING REQUIRED MODEL: {req}")
                    all_good = False
                else:
                    print(f"   ✅ Found required: {req}")
            
            # Check Forbidden
            for forb in config.get("forbidden", []):
                if forb in installed_names:
                    print(f"   ⚠️  FOUND FORBIDDEN MODEL: {forb} (Should be elsewhere)")
                    # non-fatal but noisy
            
            if not models:
                print(f"   ⚠️  No models found on {name}.")
                return False

            # Test Loaded Models
            for model in models:
                model_name = model['name']
                # Skip testing if not required (optional) or test all? 
                # User asked to "test of ALL assigned models", so we test required ones specifically.
                if model_name in config.get("required", []):
                     
                    # 2. Test Generation / Embedding
                    if "embed" in model_name.lower():
                         print(f"     > Testing embedding on {model_name}...", end="", flush=True)
                         try:
                            emb_resp = await client.post(
                                f"{url}/api/embeddings",
                                json={"model": model_name, "prompt": "Test embedding"},
                                timeout=60.0 # generous timeout for load
                            )
                            if emb_resp.status_code == 200:
                                print(" ✅ OK")
                            else:
                                print(f" ❌ FAILED ({emb_resp.status_code})")
                                all_good = False
                         except Exception as e:
                            print(f" ❌ ERROR: {e}")
                            all_good = False
                    else:
                        print(f"     > Testing inference on {model_name}...", end="", flush=True)
                        try:
                            # Use a tiny prompt
                            gen_resp = await client.post(
                                f"{url}/api/generate",
                                json={"model": model_name, "prompt": "hi", "stream": False},
                                timeout=60.0
                            )
                            if gen_resp.status_code == 200:
                                print(" ✅ OK")
                            else:
                                print(f" ❌ FAILED ({gen_resp.status_code})")
                                all_good = False
                        except Exception as e:
                            print(f" ❌ ERROR: {e}")
                            all_good = False
            
            return all_good

    except Exception as e:
        print(f"❌ Connection failed to {name}: {e}")
        return False

async def main():
    print("🔍 Verifying GPU Model Matrix...")
    
    results = await asyncio.gather(
        check_instance(GPU0_URL, EXPECTED_MATRIX[GPU0_URL]),
        check_instance(GPU1_URL, EXPECTED_MATRIX[GPU1_URL])
    )
    
    if all(results):
        print("\n✅ MATRIX VERIFIED: All assigned models loaded on correct GPUs.")
        sys.exit(0)
    else:
        print("\n❌ MATRIX FAILED: Missing models or load errors.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
