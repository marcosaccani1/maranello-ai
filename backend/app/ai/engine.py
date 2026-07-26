from app.ai.models.response import AIResponse
from app.ai.providers.base import BaseLLMProvider


class AIEngine:
    """Application component responsible for AI response generation."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        self._provider = provider

    @property
    def provider_name(self) -> str:
        """Return the configured provider class name."""

        return type(self._provider).__name__

    def generate_response(self, message: str) -> AIResponse:
        """Generate a structured response through the configured provider."""

        return self._provider.generate(message)
