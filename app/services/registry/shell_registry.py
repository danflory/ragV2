"""
Shell Registry: Formal catalog of available LLM models (Shells) with capability metadata.

A Shell is the EXECUTION ENGINE (LLM model) that powers a Ghost (Agent Identity).
This registry maps Shell identifiers to their performance characteristics,
costs, and capabilities to enable intelligent routing decisions.

Example:
    Shell: "gemma2:27b" (model specification)
    Ghost: "Librarian" (agent identity using this Shell)

The Shell Registry is purely about MODELS, not AGENTS.
For agent identities, see ghost_registry.py.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ModelTier(Enum):
    L1 = "L1"  # Local (Ollama)
    L2 = "L2"  # Cloud (DeepInfra)
    L3 = "L3"  # Frontier (Gemini)

class ModelCapability(Enum):
    GENERAL = "general"
    RAG = "rag"
    SUMMARIZATION = "summarization"
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    CODE = "code"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"
    ADVANCED_REASONING = "advanced_reasoning"
    MASSIVE_CONTEXT = "massive_context"
    CODE_REVIEW = "code_review"
    COMPLEX_TASKS = "complex_tasks"
    FAST_REASONING = "fast_reasoning"
    LARGE_CONTEXT = "large_context"

@dataclass
class ModelSpec:
    """Specification for a single model."""
    name: str
    tier: ModelTier
    cost_per_1k_tokens: float
    context_window: int
    avg_latency_ms: int
    capabilities: List[ModelCapability]
    specialty: Optional[str] = None
    vram_required_gb: Optional[int] = None
    provider: Optional[str] = None

class ShellRegistry:
    """
    Central registry of all available LLM model Shells across L1, L2, and L3 tiers.
    
    A Shell is the compute resource (model) that executes a Ghost's (agent's) intelligence.
    This registry provides specifications for routing, cost estimation, and VRAM management.
    """
    
    # L1: Local Models (Ollama)
    L1_MODELS = {
        "gemma2:27b": ModelSpec(
            name="gemma2:27b",
            tier=ModelTier.L1,
            cost_per_1k_tokens=0.0,
            context_window=8192,
            vram_required_gb=16,
            avg_latency_ms=150,
            capabilities=[
                ModelCapability.GENERAL,
                ModelCapability.RAG,
                ModelCapability.SUMMARIZATION
            ],
            specialty=None,
            provider="ollama"
        ),
        "llama3:70b": ModelSpec(
            name="llama3:70b",
            tier=ModelTier.L1,
            cost_per_1k_tokens=0.0,
            context_window=8192,
            vram_required_gb=42,
            avg_latency_ms=800,
            capabilities=[
                ModelCapability.REASONING,
                ModelCapability.ANALYSIS,
                ModelCapability.COMPLEX_TASKS
            ],
            specialty=None,
            provider="ollama"
        ),
        "qwen2.5-coder:32b": ModelSpec(
            name="qwen2.5-coder:32b",
            tier=ModelTier.L1,
            cost_per_1k_tokens=0.0,
            context_window=32768,
            vram_required_gb=20,
            avg_latency_ms=300,
            capabilities=[
                ModelCapability.CODE,
                ModelCapability.DEBUGGING,
                ModelCapability.REFACTORING
            ],
            specialty="coding",
            provider="ollama"
        )
    }
    
    # L2: Cloud Models (DeepInfra)
    L2_MODELS = {
        "meta-llama/Meta-Llama-3-70B-Instruct": ModelSpec(
            name="meta-llama/Meta-Llama-3-70B-Instruct",
            tier=ModelTier.L2,
            cost_per_1k_tokens=0.0007,
            context_window=8192,
            avg_latency_ms=400,
            capabilities=[
                ModelCapability.GENERAL,
                ModelCapability.ANALYSIS,
                ModelCapability.SUMMARIZATION
            ],
            specialty=None,
            provider="deepinfra"
        )
    }
    
    # L3: Frontier Models (Gemini)
    L3_MODELS = {
        "gemini-1.5-pro": ModelSpec(
            name="gemini-1.5-pro",
            tier=ModelTier.L3,
            cost_per_1k_tokens=0.01,
            context_window=2000000,
            avg_latency_ms=2500,
            capabilities=[
                ModelCapability.ADVANCED_REASONING,
                ModelCapability.MASSIVE_CONTEXT,
                ModelCapability.CODE_REVIEW
            ],
            specialty="frontier_intelligence",
            provider="google"
        ),
        "gemini-1.5-flash": ModelSpec(
            name="gemini-1.5-flash",
            tier=ModelTier.L3,
            cost_per_1k_tokens=0.002,
            context_window=1000000,
            avg_latency_ms=800,
            capabilities=[
                ModelCapability.FAST_REASONING,
                ModelCapability.LARGE_CONTEXT
            ],
            specialty="speed",
            provider="google"
        ),
        "claude-3-5-sonnet": ModelSpec(
            name="claude-3-5-sonnet",
            tier=ModelTier.L3,
            cost_per_1k_tokens=0.015,
            context_window=200000,
            avg_latency_ms=1500,
            capabilities=[ModelCapability.ADVANCED_REASONING, ModelCapability.CODE],
            specialty="extended_thinking",
            provider="anthropic"
        )
    }
    
    @classmethod
    def get_all_models(cls) -> Dict[str, ModelSpec]:
        """Return all models across all tiers."""
        return {
            **cls.L1_MODELS,
            **cls.L2_MODELS,
            **cls.L3_MODELS
        }
    
    @classmethod
    def get_model(cls, model_name: str) -> Optional[ModelSpec]:
        """Get a specific model by name."""
        all_models = cls.get_all_models()
        return all_models.get(model_name)
    
    @classmethod
    def get_models_by_tier(cls, tier: ModelTier) -> Dict[str, ModelSpec]:
        """Get all models for a specific tier."""
        if tier == ModelTier.L1:
            return cls.L1_MODELS
        elif tier == ModelTier.L2:
            return cls.L2_MODELS
        elif tier == ModelTier.L3:
            return cls.L3_MODELS
        return {}
    
    @classmethod
    def get_models_by_capability(cls, capability: ModelCapability) -> List[ModelSpec]:
        """Find all models that have a specific capability."""
        all_models = cls.get_all_models()
        return [
            spec for spec in all_models.values()
            if capability in spec.capabilities
        ]
    
    @classmethod
    def get_cheapest_model_for_capability(cls, capability: ModelCapability) -> Optional[ModelSpec]:
        """Find the cheapest model that has a specific capability."""
        matching = cls.get_models_by_capability(capability)
        if not matching:
            return None
        return min(matching, key=lambda m: m.cost_per_1k_tokens)
    
    @classmethod
    def estimate_cost(cls, model_name: str, token_count: int) -> float:
        """Estimate cost for a given model and token count."""
        spec = cls.get_model(model_name)
        if not spec:
            return 0.0
        return (spec.cost_per_1k_tokens * token_count) / 1000.0
    
    @classmethod
    def can_fit_in_vram(cls, model_name: str, available_vram_gb: int) -> bool:
        """Check if a model can fit in available VRAM."""
        spec = cls.get_model(model_name)
        if not spec or not spec.vram_required_gb:
            return True  # Assume cloud models don't need local VRAM
        return spec.vram_required_gb <= available_vram_gb
