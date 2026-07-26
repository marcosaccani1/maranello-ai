from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract interface implemented by every LLM provider."""

    @abstractmethod
    def generate(self, message: str) -> str:
        """Generate a response for the submitted user message."""