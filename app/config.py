from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # === GLOBAL IDENTITY ===
    USER_NAME: str = "Dan"
    PORT: int = 5050
    
    # === LAYER 1 (Local - Titan RTX) ===
    L1_URL: str = "http://127.0.0.1:11434"
    L1_MODEL: str = "codellama:7b"
    VRAM_THRESHOLD_GB: float = 2.0
    
    # === LAYER 2 (Cloud - Reasoning/Coding) ===
    L2_KEY: str | None = None
    L2_URL: str = "https://api.deepinfra.com/v1/openai/chat/completions"
    L2_MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"

    # === LAYER 3 (Agents - Google Gemini 3) ===
    L3_KEY: str | None = None
    L3_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
    L3_MODEL: str = "gemini-3-pro-preview"

    # === MEMORY (Chroma Docker) ===
    # "chroma_db" is the hostname defined in docker-compose
    CHROMA_URL: str = "http://chroma_db:8000" 
    CHROMA_COLLECTION: str = "agy_knowledge"

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Settings()