from abc import ABC, abstractmethod

class LLMDriver(ABC):
    """
    The Contract (Interface) for any AI Driver.
    """
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        pass
