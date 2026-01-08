import logging
import asyncpg
from .config import config

logger = logging.getLogger("Gravitas_DATABASE")

class Database:
    """
    Asynchronous Postgres Driver for Gravitas.
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
            
        except Exception as e:
            logger.error(f"❌ DATABASE CONNECTION FAILURE: {e}")
            self.pool = None

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("🛑 POSTGRES POOL CLOSED.")

    async def clear_history(self) -> int:
        """Deletes all rows from the history table and returns the count."""
        if not self.pool:
            return 0
        try:
            async with self.pool.acquire() as conn:
                # DELETE returns 'DELETE n' where n is the row count
                status = await conn.execute("DELETE FROM history")
                count = int(status.split()[1]) if status.startswith("DELETE") else 0
                logger.info(f"🗑️ CHAT HISTORY CLEARED: {count} messages purged.")
                return count
        except Exception as e:
            logger.error(f"❌ CLEAR HISTORY FAILURE: {e}")
            return 0

    async def get_recent_history(self, limit: int = 5):
        """Fetches the last N messages from the history table with Ghost/Shell metadata."""
        if not self.pool:
            return []
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch('''
                    SELECT role, content, ghost_id, shell_id FROM (
                        SELECT role, content, ghost_id, shell_id, timestamp 
                        FROM history 
                        ORDER BY timestamp DESC 
                        LIMIT $1
                    ) subquery
                    ORDER BY timestamp ASC
                ''', limit)
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ FETCH HISTORY FAILURE: {e}")
            return []

    async def save_history(self, role: str, content: str, ghost_id: str = "unknown_ghost", shell_id: str = "unknown_shell"):
        """
        Saves a message to the history table.
        
        Args:
            role: Message role (user/assistant/system)
            content: Message content
            ghost_id: Agent identity (Ghost name, e.g., "Librarian", "Scout")
            shell_id: Model identifier (Shell name, e.g., "gemma2:27b", "gemini-1.5-pro")
        """
        if not self.pool:
            return
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO history (role, content, ghost_id, shell_id) 
                    VALUES ($1, $2, $3, $4)
                ''', role, content, ghost_id, shell_id)
        except Exception as e:
            logger.error(f"❌ SAVE HISTORY FAILURE: {e}")

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
