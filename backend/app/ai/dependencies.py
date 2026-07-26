from functools import lru_cache

from app.ai.engine import AIEngine
from app.ai.providers.mock import MockLLMProvider


@lru_cache
def get_ai_engine() -> AIEngine:
    """Return the configured AI engine instance."""

    provider = MockLLMProvider()
    return AIEngine(provider=provider)