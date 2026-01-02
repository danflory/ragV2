import os
import sys
import subprocess
import dotenv

# Load current environment
dotenv.load_dotenv(".env")

# Define the Brain Profiles (Update names based on your 'ollama list' output)
PROFILES = {
    "coder": "qwen2.5-coder:32b",       # The "Better" Model (Heavy, High VRAM)
    "reflex": "gemma2:27b-instruct-q4_k_m", # The Standard L1 (Balanced)
    "eco": "qwen2.5-coder:7b"           # The "Low Memory" Temp (Fast, Low VRAM)
}

def get_running_model():
    """Checks what is currently set in .env"""
    return os.getenv("L1_MODEL_NAME", "Unknown")

def switch_model(profile_name):
    """Updates .env and pre-loads the model via Docker"""
    if profile_name not in PROFILES:
        print(f"❌ Unknown profile: '{profile_name}'. Available: {list(PROFILES.keys())}")
        return

    target_model = PROFILES[profile_name]
    print(f"🔄 Switching L1 from [{get_running_model()}] to [{target_model}]...")

    # 1. Update .env file
    # Note: We use simple string replacement to preserve comments/structure
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()

    with open(env_path, "w") as f:
        for line in lines:
            if line.startswith("L1_MODEL_NAME="):
                f.write(f"L1_MODEL_NAME={target_model}\n")
            else:
                f.write(line)
    
    print("✅ .env updated.")

    # 2. Pre-load model in Ollama (Warmup)
    # This forces GPU 0 to load the weights immediately
    print(f"🚀 Warming up {target_model} on Titan RTX...")
    try:
        subprocess.run(
            ["docker", "exec", "-d", "agy_ollama", "ollama", "run", target_model, ""],
            check=True
        )
        print("✅ Model loaded into VRAM.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to warm up model: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python tools/switch_brain.py [coder|reflex|eco]")
        print(f"Current: {get_running_model()}")
        sys.exit(1)
    
    switch_model(sys.argv[1])