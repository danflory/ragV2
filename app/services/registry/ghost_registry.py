"""
Ghost Registry: Catalog of Agent Identities (Roles) in the Gravitas Enterprise.

The Ghost represents the PERMANENT IDENTITY of an agent - its role, purpose, and responsibilities.
This is separate from the Shell (the LLM model that executes the role).

Example:
    Ghost: "Librarian" (role: knowledge indexing)
    Shell: "gemma2:27b" (model: executes the role)

The Ghost/Shell separation enables:
- Clean model upgrades without losing identity
- Cost tracking per role (not per model)
- Multi-tenant scenarios where different users run different Shells for the same Ghost
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class GhostRole(Enum):
    """Categories of agent roles in the Gravitas Enterprise."""
    INDEXER = "indexer"          # Knowledge acquisition and storage (Librarian)
    RESEARCHER = "researcher"    # External data acquisition (Scout)
    ORCHESTRATOR = "orchestrator" # System coordination (Supervisor)
    ANALYZER = "analyzer"        # Deep analysis and reasoning
    WRITER = "writer"            # Content generation and authoring


@dataclass
class GhostSpec:
    """Specification for a Ghost (Agent Identity)."""
    name: str                    # Human-readable identity: "Librarian", "Scout", etc.
    role: GhostRole              # Functional category
    description: str             # What this Ghost does
    preferred_shell: str         # Default Shell (model) for this Ghost
    fallback_shells: List[str]   # Alternative Shells if preferred is unavailable
    capabilities: List[str]      # What this Ghost can do
    access_level: int = 1        # Security clearance (1=basic, 5=enterprise-wide)
    is_active: bool = True       # Whether this Ghost is currently deployed


class GhostRegistry:
    """
    Central registry of all Ghost identities in the Gravitas Enterprise.
    
    This registry maps permanent agent roles to their configurations.
    Ghosts are "who" the agent is, Shells are "how" they execute.
    """
    
    # ACTIVE GHOSTS (Currently Deployed)
    ACTIVE_GHOSTS = {
        "Librarian": GhostSpec(
            name="Librarian",
            role=GhostRole.INDEXER,
            description="Knowledge indexing and document processing specialist",
            preferred_shell="gemma2:27b",
            fallback_shells=["llama3:70b", "qwen2.5-coder:32b"],
            capabilities=["document_ingestion", "chunking", "embedding", "rag_query"],
            access_level=2,
            is_active=True
        ),
        
        "Scout": GhostSpec(
            name="Scout",
            role=GhostRole.RESEARCHER,
            description="External data acquisition and web research specialist",
            preferred_shell="gemini-1.5-flash",
            fallback_shells=["gemini-1.5-pro"],
            capabilities=["web_search", "url_fetch", "content_extraction", "summarization"],
            access_level=3,
            is_active=True
        ),
        
        "Supervisor": GhostSpec(
            name="Supervisor",
            role=GhostRole.ORCHESTRATOR,
            description="System orchestration and task routing specialist",
            preferred_shell="gemini-1.5-pro",
            fallback_shells=["gemini-1.5-flash", "meta-llama/Meta-Llama-3-70B-Instruct"],
            capabilities=["task_routing", "queue_management", "agent_coordination", "certification"],
            access_level=5,
            is_active=True
        ),
    }
    
    # PLANNED GHOSTS (Future Deployment)
    PLANNED_GHOSTS = {
        "Miner": GhostSpec(
            name="Miner",
            role=GhostRole.RESEARCHER,
            description="Video/audio transcription and media extraction specialist",
            preferred_shell="gemini-1.5-pro",
            fallback_shells=["gemini-1.5-flash"],
            capabilities=["video_download", "audio_transcription", "media_indexing"],
            access_level=2,
            is_active=False
        ),
        
        "Journalist": GhostSpec(
            name="Journalist",
            role=GhostRole.ANALYZER,
            description="Deep research and analytical reporting specialist",
            preferred_shell="gemini-1.5-pro",
            fallback_shells=["meta-llama/Meta-Llama-3-70B-Instruct"],
            capabilities=["multi_source_analysis", "fact_checking", "report_generation"],
            access_level=4,
            is_active=False
        ),
        
        "Author": GhostSpec(
            name="Author",
            role=GhostRole.WRITER,
            description="Long-form content creation and book writing specialist",
            preferred_shell="gemini-1.5-pro",
            fallback_shells=["gemini-1.5-flash"],
            capabilities=["chapter_generation", "narrative_continuity", "style_consistency"],
            access_level=3,
            is_active=False
        ),
    }
    
    @classmethod
    def get_all_ghosts(cls) -> Dict[str, GhostSpec]:
        """Return all ghosts (active + planned)."""
        return {**cls.ACTIVE_GHOSTS, **cls.PLANNED_GHOSTS}
    
    @classmethod
    def get_active_ghosts(cls) -> Dict[str, GhostSpec]:
        """Return only active (deployed) ghosts."""
        return cls.ACTIVE_GHOSTS
    
    @classmethod
    def get_ghost(cls, name: str) -> Optional[GhostSpec]:
        """Get a specific ghost by name."""
        all_ghosts = cls.get_all_ghosts()
        return all_ghosts.get(name)
    
    @classmethod
    def get_ghosts_by_role(cls, role: GhostRole) -> List[GhostSpec]:
        """Find all ghosts with a specific role."""
        all_ghosts = cls.get_all_ghosts()
        return [
            spec for spec in all_ghosts.values()
            if spec.role == role
        ]
    
    @classmethod
    def get_ghost_for_capability(cls, capability: str) -> Optional[GhostSpec]:
        """Find the best ghost for a specific capability (active ghosts only)."""
        active_ghosts = cls.get_active_ghosts()
        matching = [
            spec for spec in active_ghosts.values()
            if capability in spec.capabilities
        ]
        if not matching:
            return None
        # Return highest access level (most capable)
        return max(matching, key=lambda g: g.access_level)
    
    @classmethod
    def list_ghost_names(cls) -> List[str]:
        """List all ghost names."""
        return list(cls.get_all_ghosts().keys())
    
    @classmethod
    def activate_ghost(cls, name: str) -> bool:
        """Activate a planned ghost (move to active)."""
        if name in cls.PLANNED_GHOSTS:
            ghost = cls.PLANNED_GHOSTS[name]
            ghost.is_active = True
            cls.ACTIVE_GHOSTS[name] = ghost
            del cls.PLANNED_GHOSTS[name]
            return True
        return False
