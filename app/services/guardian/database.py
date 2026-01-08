import logging
import asyncpg
from app.config import config

logger = logging.getLogger("Gravitas_DATABASE_GUARDIAN")

class Database:
    """
    Asynchronous Postgres Driver for Gravitas Guardian.
    Manages connection pooling and Guardian-specific DB operations.
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

    async def init_schema(self):
        """Initializes the database schema for the Guardian service."""
        if not self.pool:
            logger.warning("⚠️ Cannot initialize schema: Database not connected.")
            return

        try:
            async with self.pool.acquire() as conn:
                # AGENT BADGES TABLE (Phase 7 Identity)
                # Guardian Service is the Owner.
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS agent_badges (
                        id SERIAL PRIMARY KEY,
                        ghost_id VARCHAR(100) NOT NULL,
                        badge_name VARCHAR(100) NOT NULL,
                        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(ghost_id, badge_name)
                    );
                ''')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_badges_ghost ON agent_badges(ghost_id);')

                logger.info("✅ Guardian Schema Initialized (agent_badges).")
                
        except Exception as e:
            logger.error(f"❌ SCHEMA INITIALIZATION FAILURE: {e}")

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("🛑 POSTGRES POOL CLOSED.")

    def is_ready(self) -> bool:
        return self.pool is not None

# Singleton Instance
db = Database()
