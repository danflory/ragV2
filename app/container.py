from .config import config
from .L1_local import LocalLlamaDriver
from .L2_network import UniversalCloudDriver

class Container:
    def __init__(self):
        self.config = config
        
        # L1: Local Titan RTX
        self.l1_driver = LocalLlamaDriver(self.config)
        
        # L2: DeepInfra (Qwen)
        self.l2_driver = UniversalCloudDriver(
            api_key=config.L2_KEY,
            base_url=config.L2_URL,
            model=config.L2_MODEL
        )

        # L3: Google Gemini (Deep Research)
        self.l3_driver = UniversalCloudDriver(
            api_key=config.L3_KEY,
            base_url=config.L3_URL,
            model=config.L3_MODEL
        )

    def get_l1_driver(self): return self.l1_driver
    def get_l2_driver(self): return self.l2_driver
    def get_l3_driver(self): return self.l3_driver # <--- NEW
        
    def get_driver_by_tier(self, tier: str):
        tier = tier.upper()
        if tier == "L3": return self.l3_driver
        if tier == "L2": return self.l2_driver
        return self.l1_driver

container = Container()