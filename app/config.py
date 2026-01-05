from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # === GLOBAL IDENTITY ===
    USER_NAME: str = "Dan"
    PORT: int = 5050
    
    # === LAYER 1 (Local - Titan RTX) ===
    L1_URL: str = "http://ollama:11434"
    L1_MODEL: str = "codellama:7b"
    VRAM_THRESHOLD_GB: float = 2.0

    # === MODES (State Machine) ===
    MODE_RAG: str = "rag"
    MODE_DEV: str = "dev"
    DEFAULT_MODE: str = "rag"
    MODEL_MAP: dict[str, str] = {
        "rag": "gemma2:27b",
        "dev": "deepseek-coder-v2"
    }
    
    # === LAYER 2 (Cloud - Reasoning/Coding) ===
    L2_KEY: str | None = None
    L2_URL: str = "https://api.deepinfra.com/v1/openai/chat/completions"
    L2_MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"

    # === LAYER 3 (Agents - Google Gemini 3) ===
    L3_KEY: str | None = None
    L3_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"
    L3_MODEL: str = "gemini-3-pro-preview"

    # === MEMORY & STORAGE (Gravitas Grounded Research) ===
    QDRANT_HOST: str = "Gravitas_qdrant"
    QDRANT_PORT: int = 6333
    
    MINIO_ENDPOINT: str = "Gravitas_minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "gravitas-blobs"
    MINIO_SECURE: bool = False

    # Deprecated (Chroma)
    CHROMA_URL: str = "http://chroma_db:8000" 
    CHROMA_COLLECTION: str = "Gravitas_knowledge"
    DOCS_PATH: list[str] = [
        "/home/dflory/dev_env/rag_local/docs",
        "/home/dflory/dev_env/rag_local/app"
    ]

    # === DATABASE (Postgres) ===
    DB_HOST: str = "postgres_db"
    DB_PORT: int = 5432
    DB_USER: str = "agy_user"
    DB_PASS: str = "agy_pass"
    DB_NAME: str = "chat_history"

    # === GOVERNANCE (The Accountant) ===
    REF_COST_INPUT_1K: float = 0.0025
    REF_COST_OUTPUT_1K: float = 0.0100
    GRAVITAS_COST_KWH: float = 0.15

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Settings()
