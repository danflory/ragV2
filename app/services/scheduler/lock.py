import asyncio
from typing import Optional

class ModelLock:
    """
    Tracks which model is currently 'HOT' in VRAM.
    Helps prevent VRAM thrashing by identifying when a model switch is required.
    """
    def __init__(self):
        self._current_model: Optional[str] = None
        self._lock = asyncio.Lock()

    @property
    def current_model(self) -> Optional[str]:
        return self._current_model

    async def set_model(self, model_name: str):
        """
        Updates the current hot model.
        """
        async with self._lock:
            self._current_model = model_name

    def needs_switch(self, requested_model: str) -> bool:
        """
        Returns True if the requested model is different from the current hot model.
        """
        if self._current_model is None:
            return False  # No model is hot, so no "switch" (just loading)
        return self._current_model != requested_model

    async def clear(self):
        """
        Clears the current hot model (e.g., when VRAM is pruned).
        """
        async with self._lock:
            self._current_model = None
