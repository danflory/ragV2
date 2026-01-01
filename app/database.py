import logging
import asyncpg
from .config import config

logger = logging.getLogger("AGY_DATABASE")

class Database:
    """
    Asynchronous Postgres Driver for AntiGravity.
    Manages connection pooling and core DB operations.
    """
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Initializes the connection pool."""
        if self.pool:
            return

        try:
            logger.info(f"🔌 CONNECTING TO POSTGRES at {config.DB_HOST}:{config.DB_PORT}...")
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                database=config.DB_NAME,
                host=config.DB_HOST,
                port=config.DB_PORT,
                min_size=1,
                max_size=10
            )
            logger.info("✅ POSTGRES POOL READY.")
            
            # Ensure table exists (Reflexive Schema)
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS history (
                        id SERIAL PRIMARY KEY,
                        role VARCHAR(50) NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_history_timestamp ON history(timestamp);')
                
                # 2. USAGE STATS TABLE
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS usage_stats (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        model VARCHAR(100),
                        layer VARCHAR(10),
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        duration_ms INTEGER
                    );
                ''')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON usage_stats(timestamp);')
                
        except Exception as e:
            logger.error(f"❌ DATABASE CONNECTION FAILURE: {e}")
            self.pool = None

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("🛑 POSTGRES POOL CLOSED.")

    async def clear_history(self):
        """Truncates the history table."""
        if not self.pool:
            return
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("TRUNCATE TABLE history")
            logger.info("🗑️ CHAT HISTORY CLEARED.")
        except Exception as e:
            logger.error(f"❌ CLEAR HISTORY FAILURE: {e}")

    async def log_usage(self, model: str, layer: str, prompt_tokens: int, completion_tokens: int, duration_ms: int):
        """Logs model usage statistics."""
        if not self.pool:
            return
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO usage_stats (model, layer, prompt_tokens, completion_tokens, duration_ms)
                    VALUES ($1, $2, $3, $4, $5)
                ''', model, layer, prompt_tokens, completion_tokens, duration_ms)
        except Exception as e:
            logger.error(f"❌ LOG USAGE FAILURE: {e}")

    def is_ready(self) -> bool:
        return self.pool is not None

# Singleton Instance
db = Database()