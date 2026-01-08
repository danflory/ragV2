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
        """Initializes the database schema using Alembic."""
        if not self.pool:
            logger.warning("⚠️ Cannot initialize schema: Database not connected.")
            return

        try:
            # Programmatic Alembic upgrade
            import os
            from alembic.config import Config
            from alembic import command
            
            # Use absolute path to alembic.ini
            base_dir = os.path.dirname(__file__)
            alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
            alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "migrations"))
            
            # Run upgrade head
            command.upgrade(alembic_cfg, "head")
            
            logger.info("✅ Router Schema Versioned via Alembic.")
        except Exception as e:
            logger.error(f"❌ ALEMBIC MIGRATION FAILURE: {e}")

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("🛑 POSTGRES POOL CLOSED.")

    def is_ready(self) -> bool:
        return self.pool is not None

# Singleton Instance
db = Database()
