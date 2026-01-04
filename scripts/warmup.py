import subprocess
import sys
import os
import time

# Ensure we can import the logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.system_log import log_system_event
from app.config import config

# SETTINGS
# Increased to 60s based on real-world observation of 16B model load times.
TIMEOUT_SECONDS = 60

def warmup_brain():
    model = config.L1_MODEL
    print(f"   [...] 🧠 Pinging {model} (Timeout: {TIMEOUT_SECONDS}s)...")
    
    start_ts = time.time()
    try:
        # Run a silent "hello"
        subprocess.run(
            ["ollama", "run", model, "hello"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT_SECONDS,
            check=True
        )
        duration = time.time() - start_ts
        msg = f"Model loaded in {duration:.2f}s"
        print(f"   [OK] ✅ {msg}")
        log_system_event("WARMUP_SUCCESS", "warmup.py", msg)
        
    except subprocess.TimeoutExpired:
        msg = f"Warm-up TIMED OUT after {TIMEOUT_SECONDS}s. GPU likely stuck."
        print(f"   [!!] ❌ {msg}")
        log_system_event("WARMUP_FAIL", "warmup.py", msg)
        # We exit with 0 (success) because we don't want to stop the server from starting,
        # we just want to warn the user that the brain is sluggish.
        
    except Exception as e:
        msg = f"Warm-up Failed: {str(e)}"
        print(f"   [!!] ❌ {msg}")
        log_system_event("WARMUP_ERROR", "warmup.py", msg)

if __name__ == "__main__":
    warmup_brain()