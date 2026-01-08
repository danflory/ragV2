#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import httpx
from google import genai
import logging

# Ensure we can import app components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.config import config as app_config

logger = logging.getLogger(__name__)

class ModelInventoryTool:
    """Tool to list and verify all models across Gravitas tiers."""
    
    def __init__(self):
        self.config = {
            'L1_URL': app_config.L1_URL,
            'L1_MODEL': app_config.L1_MODEL,
            'L2_KEY': app_config.L2_KEY,
            'L2_MODEL': app_config.L2_MODEL,
            'L3_KEY': app_config.L3_KEY,
            'L3_MODEL': app_config.L3_MODEL,
        }

    def _list_ollama_models(self, url, description):
        """List models from a specific Ollama instance."""
        print(f"\n🖥️  {description} ({url})")
        print("=" * 50)
        try:
            response = httpx.get(f"{url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                if models:
                    for model in models:
                        name = model.get('name', 'Unknown')
                        size = model.get('size', 0)
                        size_gb = size / (1024**3) if size > 0 else 0
                        print(f"  🧠 {name} ({size_gb:.1f} GB)")
                else:
                    print("  ❌ No models found")
            else:
                print(f"  ❌ Failed to connect: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    def _check_deepinfra_models(self):
        """Check DeepInfra models (L2)."""
        print("\n☁️  L2 Cloud Models (DeepInfra)")
        print("=" * 40)
        api_key = self.config['L2_KEY']
        if not api_key:
            print("  ❌ No API key configured")
            return
            
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = httpx.get("https://api.deepinfra.com/v1/models", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                qwen_models = [m for m in models if 'qwen' in m['id'].lower()]
                
                print(f"  🎯 Configured Model: {self.config['L2_MODEL']}")
                if qwen_models:
                    print("  📋 Available Qwen Models:")
                    for model in qwen_models[:5]:
                        print(f"     • {model['id']}")
                    if len(qwen_models) > 5:
                        print(f"     ... and {len(qwen_models) - 5} more")
            else:
                print(f"  ❌ API Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Connection Error: {e}")

    def _check_google_models(self):
        """Check Google Gemini models (L3)."""
        print("\n☁️  L3 Cloud Models (Google Gemini)")
        print("=" * 40)
        api_key = self.config['L3_KEY']
        if not api_key:
            print("  ❌ No API key configured")
            return
            
        try:
            client = genai.Client(api_key=api_key)
            pager = client.models.list()
            print(f"  🎯 Configured Model: {self.config['L3_MODEL']}")
            print("  📋 Available Gemini Models:")
            
            count = 0
            for model in pager:
                if "gemini" in model.name.lower() and "vision" not in model.name.lower():
                    print(f"     • {model.name.replace('models/', '')}")
                    count += 1
                    if count >= 5: break
            if count == 0: print("     No Gemini models found")
        except Exception as e:
            print(f"  ❌ API Error: {e}")

    def execute(self):
        print("🤖 Gravitas RAG - Model Inventory")
        print("=" * 50)
        
        # Local main Ollama
        self._list_ollama_models(self.config['L1_URL'], "GPU 0 (Generation)")
        
        # local embedding/aux Ollama (often on port 11435)
        # We check if 11435 is in use
        self._list_ollama_models("http://localhost:11435", "GPU 1 (Embeddings)")
        
        self._check_deepinfra_models()
        self._check_google_models()
        print("\n✅ Model inventory complete!")

if __name__ == "__main__":
    tool = ModelInventoryTool()
    tool.execute()
