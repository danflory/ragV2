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

import os
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from app.services.registry.model_schema import ModelsConfig, ModelDefinition

logger = logging.getLogger("Gravitas_SHELL_REGISTRY")


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
    
    Loads model definitions from app/config/models.yaml for dynamic configuration.
    """
    
    # Class variables to store loaded models
    L1_MODELS: Dict[str, ModelSpec] = {}
    L2_MODELS: Dict[str, ModelSpec] = {}
    L3_MODELS: Dict[str, ModelSpec] = {}
    _loaded: bool = False
    
    @classmethod
    def _load_models_from_yaml(cls):
        """Load models from YAML configuration file."""
        if cls._loaded:
            return
        
        # Get config file path
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "config",
            "models.yaml"
        )
        
        if not os.path.exists(config_path):
            logger.error(f"❌ Model config not found: {config_path}")
            logger.warning("⚠️ Using empty model registry")
            cls._loaded = True
            return
        
        try:
            # Load and parse YAML
            with open(config_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
            
            # Validate with Pydantic
            config = ModelsConfig(**yaml_data)
            
            # Convert to ModelSpec objects and organize by tier
            for model_def in config.models:
                # Convert capability strings to enums
                capabilities = []
                for cap_str in model_def.capabilities:
                    try:
                        capabilities.append(ModelCapability(cap_str))
                    except ValueError:
                        logger.warning(f"⚠️ Unknown capability '{cap_str}' for model {model_def.name}")
                
                # Create ModelSpec
                spec = ModelSpec(
                    name=model_def.name,
                    tier=ModelTier(model_def.tier),
                    cost_per_1k_tokens=model_def.cost_per_1k_tokens,
                    context_window=model_def.context_window,
                    avg_latency_ms=model_def.avg_latency_ms,
                    capabilities=capabilities,
                    specialty=model_def.specialty,
                    vram_required_gb=model_def.vram_required_gb,
                    provider=model_def.provider
                )
                
                # Add to appropriate tier
                if spec.tier == ModelTier.L1:
                    cls.L1_MODELS[model_def.name] = spec
                elif spec.tier == ModelTier.L2:
                    cls.L2_MODELS[model_def.name] = spec
                elif spec.tier == ModelTier.L3:
                    cls.L3_MODELS[model_def.name] = spec
            
            cls._loaded = True
            logger.info(f"✅ Loaded {len(config.models)} models from {config_path}")
            logger.info(f"   L1: {len(cls.L1_MODELS)}, L2: {len(cls.L2_MODELS)}, L3: {len(cls.L3_MODELS)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model config: {e}")
            logger.warning("⚠️ Using empty model registry")
            cls._loaded = True
    
    @classmethod
    def get_all_models(cls) -> Dict[str, ModelSpec]:
        """Return all models across all tiers."""
        cls._load_models_from_yaml()
        return {
            **cls.L1_MODELS,
            **cls.L2_MODELS,
            **cls.L3_MODELS
        }
    
    @classmethod
    def get_model(cls, model_name: str) -> Optional[ModelSpec]:
        """Get a specific model by name."""
        cls._load_models_from_yaml()
        all_models = cls.get_all_models()
        return all_models.get(model_name)
    
    @classmethod
    def get_models_by_tier(cls, tier: ModelTier) -> Dict[str, ModelSpec]:
        """Get all models for a specific tier."""
        cls._load_models_from_yaml()
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
        cls._load_models_from_yaml()
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
    
    @classmethod
    def reload_config(cls):
        """Force reload of model configuration from YAML."""
        cls._loaded = False
        cls.L1_MODELS = {}
        cls.L2_MODELS = {}
        cls.L3_MODELS = {}
        cls._load_models_from_yaml()
        logger.info("🔄 Model registry reloaded from config")
