import logging
import asyncpg
from app.config import config

logger = logging.getLogger("Gravitas_DATABASE_ROUTER")

class Database:
    """
    Asynchronous Postgres Driver for Gravitas Router.
    Provisional owner of shared tables until full decomposition.
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
        """Initializes the database schema for the Router service."""
        if not self.pool:
            logger.warning("⚠️ Cannot initialize schema: Database not connected.")
            return

        try:
            async with self.pool.acquire() as conn:
                # 1. CHAT HISTORY TABLE
                # (Lobby Service Future Owner)
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS history (
                        id SERIAL PRIMARY KEY,
                        role VARCHAR(50) NOT NULL,
                        content TEXT NOT NULL,
                        ghost_id VARCHAR(100) DEFAULT 'unknown_ghost',
                        shell_id VARCHAR(100) DEFAULT 'unknown_shell',
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                await conn.execute('ALTER TABLE history ADD COLUMN IF NOT EXISTS ghost_id VARCHAR(100) DEFAULT \'unknown_ghost\';')
                await conn.execute('ALTER TABLE history ADD COLUMN IF NOT EXISTS shell_id VARCHAR(100) DEFAULT \'unknown_shell\';')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_history_timestamp ON history(timestamp);')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_history_ghost ON history(ghost_id);')
                
                # 2. USAGE STATS TABLE
                # (Telemetry Service Provisional Owner)
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
                
                # 3. SYSTEM TELEMETRY TABLE
                # (Telemetry Service Provisional Owner)
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS system_telemetry (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        event_type VARCHAR(100) NOT NULL,
                        component VARCHAR(50),
                        value NUMERIC,
                        metadata JSONB,
                        status VARCHAR(20)
                    );
                ''')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON system_telemetry(timestamp);')

                logger.info("✅ Router Schema Initialized.")
                
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
