RAG development
Custom Gem
I acknowledge receipt of the second half of the tests/ directory (11 files).

Full System Audit Complete. I now possess the complete DNA of Gravitas v4.0. The forensic analysis of the test suite (test_hybrid_search.py vs test_memory_logic.py) confirms the architectural gap: you have Unit Tests for the Future (Qdrant) running against Legacy Code (Chroma).

To close this gap without "Spaghetti Code," I have generated the Architectural Artifacts (Interfaces & Templates). These are the non-negotiable blueprints the Coder must follow.

Step 1: The New Laws (app/interfaces.py)
Current State: The file only defines LLMDriver. New State: We must define the Contracts for Storage (MinIO) and Memory (Qdrant) to enforce Dependency Injection.


from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class LLMDriver(ABC):
    """Contract for AI Models (L1/L2/L3)."""
    @abstractmethod
    async def generate(self, prompt: str) -> str: pass
    @abstractmethod
    async def check_health(self) -> bool: pass

class ObjectStore(ABC):
    """Contract for Blob Storage (MinIO/S3)."""
    @abstractmethod
    async def upload(self, key: str, data: str) -> bool:
        """Uploads raw text content."""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Retrieves raw text content."""
        pass

class VectorMemory(ABC):
    """Contract for Vector Database (Qdrant)."""
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[str]:
        """Returns relevant text chunks."""
        pass

    @abstractmethod
    async def ingest(self, text: str, metadata: Dict[str, Any]) -> bool:
        """
        Gravitas Grounded Research Logic:
        1. Upload text to ObjectStore.
        2. Embed text.
        3. Upload embedding + metadata to VectorDB.
        """
        pass