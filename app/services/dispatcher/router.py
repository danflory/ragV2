from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TargetModel(Enum):
    L1 = "L1"  # Local (e.g., gemma2:27b via Ollama)
    L2 = "L2"  # Network/Cloud (e.g., DeepInfra - Faster/Cheaper)
    L3 = "L3"  # High Intelligence (e.g., Gemini 1.5 Pro - Expensive/Powerful)

@dataclass
class TelemetryState:
    vram_usage_percent: float
    system_load_percent: float
    avg_latency: float

@dataclass
class UserQuery:
    text: str
    code_complexity: int = 5  # Estimated or analyzed complexity

class DispatcherRouter:
    """
    State-less logic for routing user queries to the appropriate model tier.
    """
    def route(self, query: UserQuery, telemetry: TelemetryState) -> TargetModel:
        # Rule A: If code_complexity > 8 -> L3 (Highest intelligence required)
        if query.code_complexity > 8:
            return TargetModel.L3
        
        # Rule B: If system_load > 90% -> L2 (Offload to cloud to save local resources)
        if telemetry.system_load_percent > 90:
            return TargetModel.L2
            
        # Rule C: Default -> L1 (Local processing)
        return TargetModel.L1
