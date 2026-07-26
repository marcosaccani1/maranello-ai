from app.ai.providers.base import BaseLLMProvider
from app.ai.providers.mock import MockLLMProvider
from app.ai.providers.openai import OpenAIProvider
from app.core.config import Settings


class UnsupportedLLMProviderError(ValueError):
    """Raised when the configured LLM provider is not supported."""


def create_llm_provider(settings: Settings) -> BaseLLMProvider:
    """Create the LLM provider selected through application settings."""

    if settings.llm_provider == "mock":
        return MockLLMProvider(model=settings.llm_model)

    if settings.llm_provider == "openai":
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.llm_model,
            timeout_seconds=settings.llm_timeout_seconds,
        )

    raise UnsupportedLLMProviderError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
