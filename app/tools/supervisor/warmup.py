import subprocess
import sys
import os
import time
import logging

# Ensure we can import app components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.system_log import log_system_event
from app.config import config

logger = logging.getLogger(__name__)

class ModelWarmupTool:
    """Tool to warm up LLM models (primarily L1/Ollama)."""
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.model = config.L1_MODEL

    def execute(self):
        """Warms up the L1 model by sending a simple ping."""
        print(f"   [...] 🧠 Pinging {self.model} (Timeout: {self.timeout}s)...")
        
        start_ts = time.time()
        try:
            # Run a silent "hello"
            subprocess.run(
                ["ollama", "run", self.model, "hello"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout,
                check=True
            )
            duration = time.time() - start_ts
            msg = f"Model loaded in {duration:.2f}s"
            print(f"   [OK] ✅ {msg}")
            log_system_event("WARMUP_SUCCESS", "ModelWarmupTool", msg)
            return True, msg
            
        except subprocess.TimeoutExpired:
            msg = f"Warm-up TIMED OUT after {self.timeout}s. GPU likely stuck."
            print(f"   [!!] ❌ {msg}")
            log_system_event("WARMUP_FAIL", "ModelWarmupTool", msg)
            return False, msg
            
        except Exception as e:
            msg = f"Warm-up Failed: {str(e)}"
            print(f"   [!!] ❌ {msg}")
            log_system_event("WARMUP_ERROR", "ModelWarmupTool", msg)
            return False, msg

if __name__ == "__main__":
    tool = ModelWarmupTool()
    tool.execute()
