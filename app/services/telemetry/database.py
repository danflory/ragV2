"""
Gravitas Telemetry Service - Database Manager
Manages PostgreSQL connection and schema for telemetry tables.
"""
import logging
import asyncpg
from app.config import config

logger = logging.getLogger("Gravitas_TELEMETRY_DATABASE")


class TelemetryDatabase:
    """Database manager for telemetry service."""
    
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Initialize connection pool to PostgreSQL."""
        if self.pool:
            return

        try:
            logger.info(f"🔌 Connecting to PostgreSQL at {config.DB_HOST}:{config.DB_PORT}...")
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                database=config.DB_NAME,
                host=config.DB_HOST,
                port=config.DB_PORT,
                min_size=2,
                max_size=10
            )
            logger.info("✅ PostgreSQL connection pool ready")
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            self.pool = None

    async def init_schema(self):
        """
        Initialize telemetry database schema.
        Creates system_telemetry and usage_stats tables.
        """
        if not self.pool:
            logger.warning("⚠️ Cannot initialize schema: Database not connected")
            return

        try:
            async with self.pool.acquire() as conn:
                # Create system_telemetry table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS system_telemetry (
                        id SERIAL PRIMARY KEY,
                        event_type VARCHAR(50) NOT NULL,
                        component VARCHAR(100),
                        value FLOAT,
                        metadata JSONB,
                        status VARCHAR(20),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index on timestamp for efficient queries
                await conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp 
                    ON system_telemetry(timestamp DESC)
                ''')
                
                # Create index on component for filtering
                await conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_telemetry_component 
                    ON system_telemetry(component)
                ''')
                
                # Create usage_stats table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS usage_stats (
                        id SERIAL PRIMARY KEY,
                        ghost_id VARCHAR(100),
                        shell_id VARCHAR(100),
                        model_name VARCHAR(100),
                        tokens_input INTEGER,
                        tokens_output INTEGER,
                        cost_usd FLOAT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index on timestamp for usage stats
                await conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_usage_timestamp 
                    ON usage_stats(timestamp DESC)
                ''')
                
                logger.info("✅ Telemetry schema initialized (system_telemetry, usage_stats)")
                
        except Exception as e:
            logger.error(f"❌ Schema initialization failed: {e}")

    async def disconnect(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("🛑 PostgreSQL connection pool closed")

    def is_ready(self) -> bool:
        """Check if database is ready."""
        return self.pool is not None


# Singleton instance
db = TelemetryDatabase()
