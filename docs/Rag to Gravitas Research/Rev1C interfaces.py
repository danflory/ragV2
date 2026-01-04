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
        Omni-RAG Logic:
        1. Upload text to ObjectStore.
        2. Embed text.
        3. Upload embedding + metadata to VectorDB.
        """
        pass