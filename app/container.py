import logging
from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import DeepInfraDriver
from .memory import VectorStore, save_interaction, retrieve_short_term_memory
from .ingestor import DocumentIngestor
from .telemetry import telemetry

logger = logging.getLogger("AGY_CONTAINER")

class Container:
    """
    The IoC Container (Switchboard).
    """
    def __init__(self):
        logger.info("🔧 INTIALIZING DEPENDENCY CONTAINER...")
        
        # 1. LAYER 1: LOCAL REFLEX (Ollama)
        self.l1_driver = LocalLlamaDriver(config=config)

        # 2. LAYER 2: REASONING (DeepInfra)
        self.l2_driver = DeepInfraDriver(
            api_key=config.L2_KEY,
            base_url=config.L2_URL,
            model=config.L2_MODEL
        )
        
        # 3. MEMORY: VECTOR STORE (Chroma)
        try:
            self.memory = VectorStore()
        except Exception as e:
            logger.error(f"⚠️ RUNNING WITHOUT VECTOR MEMORY: {e}")
            self.memory = None
            
        # 4. INGESTOR
        if self.memory:
            self.ingestor = DocumentIngestor(self.memory)
        else:
            self.ingestor = None

        # 5. TELEMETRY
        self.telemetry = telemetry

        logger.info("✅ CONTAINER READY.")

# Singleton Instance
container = Container()
