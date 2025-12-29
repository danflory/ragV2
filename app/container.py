from .config import config
from .L1_local import L1Driver

class ServiceContainer:
    """
    The Central Switchboard (IoC Container).
    Responsible for initializing all drivers with their configuration.
    """
    def __init__(self):
        # --- Wire up Layer 1 (Local) ---
        # The container reads the config and injects it into the driver.
        self.l1_driver = L1Driver(
            base_url=config.OLLAMA_BASE_URL,
            model_name=config.MODEL
        )
        
        # (Future Placeholders for L2 and L3)
        self.l2_driver = None 
        self.l3_driver = None

# Create the global instance
container = ServiceContainer()