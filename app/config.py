import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class CONFIG:
    # --- Server Settings ---
    PORT = 5050
    USER_NAME = os.getenv("USER_NAME", "Dan")
    
    # --- LAYER 1: LOCAL ---
    MODEL = os.getenv("L1_MODEL", "codellama:7b")
    
    # FAIL-SAFE CHANGE: Default is now explicitly 127.0.0.1
    # This fixes the connection even if .env is missing/ignored
    OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    
    # --- LAYER 2: CLOUD ---
    L2_KEY = os.getenv("DEEPINFRA_API_KEY")
    
    # --- LAYER 3: STRATEGY ---
    L3_KEY = os.getenv("GOOGLE_API_KEY")

    # --- HARDWARE ---
    VRAM_THRESHOLD_GB = 4.0 
    
    # --- STORAGE ---
    CHROMA_PATH = os.path.expanduser("~/dev_env/rag_local/chroma_db")
    SQLITE_DB_PATH = "memory.db"
    CHAT_HISTORY_LIMIT = 25
    SEMANTIC_MATCH_THRESHOLD = 0.85

config = CONFIG()