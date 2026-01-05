import logging
from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import DeepInfraDriver
from .L3_google import GoogleGeminiDriver
from .memory import QdrantVectorStore, save_interaction, retrieve_short_term_memory
from .storage import MinioConnector
from .ingestor import DocumentIngestor
from .telemetry import telemetry

logger = logging.getLogger("Gravitas_CONTAINER")

class Container:
    """
    The IoC Container (Switchboard).
    Updated for Gravitas Grounded Research Phase 4.1.
    """
    def __init__(self):
        logger.info("🔧 INITIALIZING DEPENDENCY CONTAINER (Gravitas Grounded Research Phase 4.1)...")
        
        # 1. LAYER 1: LOCAL REFLEX (Ollama)
        try:
            self.l1_driver = LocalLlamaDriver(config=config)
            logger.info("✅ L1 Driver (LocalLlama) READY.")
        except Exception as e:
            logger.error(f"❌ L1 Driver initialization failed: {e}")
            raise

        # 2. LAYER 2: REASONING (DeepInfra)
        try:
            self.l2_driver = DeepInfraDriver(
                api_key=config.L2_KEY,
                base_url=config.L2_URL,
                model=config.L2_MODEL
            )
            logger.info("✅ L2 Driver (DeepInfra) READY.")
        except Exception as e:
            logger.error(f"❌ L2 Driver initialization failed: {e}")
            raise

        # 3. LAYER 3: DEEP RESEARCH (Google Gemini)
        try:
            self.l3_driver = GoogleGeminiDriver(
                api_key=config.L3_KEY,
                model=config.L3_MODEL
            )
            logger.info("✅ L3 Driver (Google Gemini) READY.")
        except Exception as e:
            logger.error(f"❌ L3 Driver initialization failed: {e}")
            raise
        
        # 4. STORAGE: BLOB STORE (MinIO)
        try:
            self.storage = MinioConnector(
                endpoint=config.MINIO_ENDPOINT,
                access_key=config.MINIO_ACCESS_KEY,
                secret_key=config.MINIO_SECRET_KEY,
                bucket_name=config.MINIO_BUCKET,
                secure=config.MINIO_SECURE
            )
            logger.info("✅ STORAGE (MinIO) READY.")
        except Exception as e:
            logger.error(f"❌ STORAGE INIT FAILURE: {e}")
            self.storage = None

        # 5. MEMORY: VECTOR STORE (Qdrant)
        try:
            if self.storage:
                self.memory = QdrantVectorStore(
                    storage=self.storage,
                    host=config.QDRANT_HOST,
                    port=config.QDRANT_PORT
                )
                logger.info("✅ MEMORY (Qdrant) READY.")
            else:
                logger.warning("⚠️ Cannot initialize memory without valid storage connector.")
                self.memory = None
        except Exception as e:
            logger.error(f"⚠️ RUNNING WITHOUT VECTOR MEMORY: {e}")
            self.memory = None
            
        # 6. INGESTOR
        try:
            if self.memory and self.storage:
                self.ingestor = DocumentIngestor(
                    vector_store=self.memory, 
                    storage=self.storage
                )
                logger.info("✅ INGESTOR READY.")
            else:
                logger.warning("⚠️ Cannot initialize ingestor without valid memory and storage.")
                self.ingestor = None
        except Exception as e:
            logger.error(f"❌ INGESTOR INIT FAILURE: {e}")
            self.ingestor = None

        # 7. TELEMETRY
        try:
            self.telemetry = telemetry
            logger.info("✅ TELEMETRY READY.")
        except Exception as e:
            logger.error(f"❌ TELEMETRY INIT FAILURE: {e}")
            self.telemetry = None

        # 8. STATE MANAGEMENT
        self.current_mode = config.DEFAULT_MODE

        # 9. AGENTS: THE LIBRARIAN
        try:
            from .agents.librarian import LibrarianAgent
            self.librarian = LibrarianAgent(container=self)
            logger.info("✅ LIBRARIAN AGENT READY.")
        except Exception as e:
            logger.error(f"❌ LIBRARIAN AGENT INIT FAILURE: {e}")
            self.librarian = None

        # 10. AGENTS: THE SCOUT
        try:
            from .agents.scout import ScoutAgent
            self.scout = ScoutAgent(l3_driver=self.l3_driver, memory=self.memory)
            logger.info("✅ SCOUT AGENT READY.")
        except Exception as e:
            logger.error(f"❌ SCOUT AGENT INIT FAILURE: {e}")
            self.scout = None

        logger.info(f"✅ CONTAINER READY (Mode: {self.current_mode}).")

    async def switch_mode(self, target_mode: str) -> bool:
        """
        Mutually Exclusive Mode Switch (VRAM Management).
        """
        if target_mode == self.current_mode:
            logger.info(f"Already in {target_mode} mode.")
            return True
        
        # Resolve model name from config
        new_model = config.MODEL_MAP.get(target_mode)
        if not new_model:
            logger.error(f"Unknown mode: {target_mode}")
            return False
            
        logger.info(f"🔄 SWITCHING SYSTEM MODE: {self.current_mode} -> {target_mode}")
        
        # Switch model in L1
        success = await self.l1_driver.load_model(new_model)
        if success:
            self.current_mode = target_mode
            logger.info(f"✅ Mode switched to {target_mode}")
            return True
        else:
            logger.error(f"❌ Failed to switch mode to {target_mode}")
            return False

# Singleton Instance
container = Container()
