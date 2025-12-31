import logging
from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import DeepInfraDriver

logger = logging.getLogger("AGY_CONTAINER")

class Container:
    """
    The IoC Container (Switchboard).
    Initializes all drivers once and holds them in memory.
    """
    def __init__(self):
        logger.info("🔧 INTIALIZING DEPENDENCY CONTAINER...")
        
        # 1. LAYER 1: LOCAL REFLEX (Ollama)
        # FIX: Pass the entire 'config' object as required by LocalLlamaDriver
        self.l1_driver = LocalLlamaDriver(config=config)

        # 2. LAYER 2: REASONING (DeepInfra)
        # DeepInfraDriver takes explicit arguments (as defined in L2_network.py)
        self.l2_driver = DeepInfraDriver(
            api_key=config.L2_KEY,
            base_url=config.L2_URL,
            model=config.L2_MODEL
        )
        
        logger.info("✅ CONTAINER READY: L1 + L2 Drivers Loaded.")

# Singleton Instance
container = Container()