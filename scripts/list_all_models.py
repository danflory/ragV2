#!/usr/bin/env python3
"""
Gravitas RAG - Comprehensive Model Inventory Script
Lists all inference models across local (Ollama) and cloud (API) layers.
"""

import os
import sys
import subprocess
import json
import httpx
from google import genai

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_env_vars():
    """Load environment variables from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value.strip('"\'')
    
    # Load from actual environment or .env
    return {
        'L1_URL': os.getenv('L1_URL', 'http://localhost:11434'),
        'L1_MODEL': os.getenv('L1_MODEL', 'codellama:7b'),
        'L2_KEY': os.getenv('L2_KEY'),
        'L2_URL': os.getenv('L2_URL', 'https://api.deepinfra.com/v1/openai/chat/completions'),
        'L2_MODEL': os.getenv('L2_MODEL', 'Qwen/Qwen2.5-Coder-32B-Instruct'),
        'L3_KEY': os.getenv('L3_KEY'),
        'L3_URL': os.getenv('L3_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent'),
        'L3_MODEL': os.getenv('L3_MODEL', 'gemini-3-pro-preview'),
    }

def list_ollama_models(url, gpu_name):
    """List models from Ollama instance"""
    try:
        print(f"\n🖥️  {gpu_name} Ollama Models ({url})")
        print("=" * 50)
        
        # Use curl to get models in JSON format
        result = subprocess.run(
            ['curl', '-s', f'{url}/api/tags'], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'models' in data and data['models']:
                for model in data['models']:
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 0)
                    modified = model.get('modified', 'Unknown')
                    # Convert size to GB for readability
                    size_gb = size / (1024**3) if size > 0 else 0
                    print(f"  🧠 {name}")
                    print(f"     Size: {size_gb:.1f} GB")
                    print(f"     Modified: {modified}")
                    print()
            else:
                print("  ❌ No models found")
        else:
            print(f"  ❌ Failed to connect: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"  ❌ Timeout connecting to {url}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def check_deepinfra_models(api_key, configured_model):
    """Check DeepInfra (L2) models"""
    print("\n☁️  L2 Cloud Models (DeepInfra)")
    print("=" * 40)
    
    if not api_key:
        print("  ❌ No API key configured")
        return
        
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = httpx.get("https://api.deepinfra.com/v1/models", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            qwen_models = [m for m in models if 'qwen' in m['id'].lower() or 'Qwen' in m['id']]
            
            print(f"  🎯 Configured Model: {configured_model}")
            if qwen_models:
                print("  📋 Available Qwen Models:")
                for model in qwen_models[:5]:  # Show top 5
                    print(f"     • {model['id']}")
                if len(qwen_models) > 5:
                    print(f"     ... and {len(qwen_models) - 5} more")
            else:
                print("  ⚠️  No Qwen models found in API response")
        else:
            print(f"  ❌ API Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Connection Error: {e}")

def check_google_models(api_key, configured_model):
    """Check Google Gemini (L3) models"""
    print("\n☁️  L3 Cloud Models (Google Gemini)")
    print("=" * 40)
    
    if not api_key:
        print("  ❌ No API key configured")
        return
        
    try:
        client = genai.Client(api_key=api_key)
        pager = client.models.list()
        
        print(f"  🎯 Configured Model: {configured_model}")
        print("  📋 Available Gemini Models:")
        
        gemini_count = 0
        for model in pager:
            if "gemini" in model.name.lower() and "vision" not in model.name.lower():
                model_name = model.name.replace('models/', '')
                print(f"     • {model_name}")
                gemini_count += 1
                if gemini_count >= 5:  # Limit output
                    break
                    
        if gemini_count == 0:
            print("     No Gemini models found")
            
    except Exception as e:
        print(f"  ❌ API Error: {e}")

def main():
    print("🤖 Gravitas RAG - Model Inventory")
    print("=" * 50)
    
    # Load configuration
    config = load_env_vars()
    
    # List local models (GPU 0 - Generation)
    list_ollama_models("http://localhost:11434", "GPU 0 (Titan RTX)")
    
    # List embedding models (GPU 1 - Embeddings)
    list_ollama_models("http://localhost:11435", "GPU 1 (GTX 1060)")
    
    # Check cloud models
    check_deepinfra_models(config['L2_KEY'], config['L2_MODEL'])
    check_google_models(config['L3_KEY'], config['L3_MODEL'])
    
    print("\n📋 Summary")
    print("=" * 20)
    print("✅ Model inventory complete!")
    print("💡 Tip: Use 'ollama pull <model>' to download new models")

if __name__ == "__main__":
    main()
