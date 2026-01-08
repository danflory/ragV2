"""
Model Configuration Schema
Pydantic models for validating YAML model definitions.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ModelTierEnum(str, Enum):
    """Model tier classification."""
    L1 = "L1"  # Local (Ollama)
    L2 = "L2"  # Cloud (DeepInfra, etc.)
    L3 = "L3"  # Frontier (Gemini, Claude)


class ModelProviderEnum(str, Enum):
    """Model provider."""
    OLLAMA = "ollama"
    DEEPINFRA = "deepinfra"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"


class ModelDefinition(BaseModel):
    """Single model specification from YAML."""
    name: str = Field(..., description="Model identifier (e.g., 'gemma2:27b')")
    tier: ModelTierEnum = Field(..., description="Model tier (L1/L2/L3)")
    provider: ModelProviderEnum = Field(..., description="Provider (ollama/google/anthropic/deepinfra)")
    
    # Cost (optional, defaults to 0 for local models)
    cost_per_1k_tokens: float = Field(0.0, description="Cost per 1000 tokens")
    
    # Context and performance
    context_window: int = Field(8192, description="Maximum context window size")
    avg_latency_ms: int = Field(500, description="Average latency in milliseconds")
    
    # Capabilities
    capabilities: List[str] = Field(default_factory=list, description="Model capabilities")
    specialty: Optional[str] = Field(None, description="Special focus area")
    
    # Local model specifics
    vram_required_gb: Optional[int] = Field(None, description="VRAM required for local models")
    
    class Config:
        use_enum_values = True


class ModelsConfig(BaseModel):
    """Root configuration containing all models."""
    models: List[ModelDefinition] = Field(..., description="List of all available models")
    
    class Config:
        use_enum_values = True
