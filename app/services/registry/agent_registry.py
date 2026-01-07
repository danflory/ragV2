"""
Agent Registry (DEPRECATED - BACKWARD COMPATIBILITY FACADE)

This module provides backward compatibility for code that still imports AgentRegistry.

MIGRATION PATH:
- New code should import from ghost_registry.py (for agent identities) 
  and shell_registry.py (for model specifications)
- This facade will be removed in Phase 7

For the new architecture:
    Ghost = Agent Identity (Who) → see ghost_registry.py
    Shell = Model/Runtime (How) → see shell_registry.py
"""

import warnings
from app.services.registry.shell_registry import ShellRegistry
from app.services.registry.ghost_registry import GhostRegistry

# Issue deprecation warning
warnings.warn(
    "AgentRegistry is deprecated. Use GhostRegistry for agent identities "
    "and ShellRegistry for model specifications. "
    "This compatibility layer will be removed in Phase 7.",
    DeprecationWarning,
    stacklevel=2
)

# Provide backward compatibility by aliasing to ShellRegistry
# (Most code using "AgentRegistry" was actually querying model specs)
AgentRegistry = ShellRegistry

# Also expose the enums for backward compatibility
from app.services.registry.shell_registry import ModelTier, ModelCapability, ModelSpec

__all__ = [
    "AgentRegistry",  # Deprecated alias for ShellRegistry
    "GhostRegistry",  # New: Agent identities
    "ShellRegistry",  # New: Model specifications
    "ModelTier",
    "ModelCapability",
    "ModelSpec"
]
