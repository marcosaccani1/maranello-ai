from abc import ABC, abstractmethod

from app.ai.models.response import AIResponse


class BaseLLMProvider(ABC):
    """Abstract interface implemented by every LLM provider."""

    @abstractmethod
    def generate(self, message: str) -> AIResponse:
        """Generate a provider-independent response."""