from app.ai.providers.base import BaseLLMProvider
from app.ai.providers.mock import MockLLMProvider
from app.core.config import Settings


class UnsupportedLLMProviderError(ValueError):
    """Raised when the configured LLM provider is not supported."""


def create_llm_provider(settings: Settings) -> BaseLLMProvider:
    """Create the LLM provider selected through application settings."""

    if settings.llm_provider == "mock":
        return MockLLMProvider(model=settings.llm_model)

    raise UnsupportedLLMProviderError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )