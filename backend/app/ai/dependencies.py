from functools import lru_cache

from app.ai.engine import AIEngine
from app.ai.providers.factory import create_llm_provider
from app.core.config import get_settings


@lru_cache
def get_ai_engine() -> AIEngine:
    """Return the AI engine configured through environment settings."""

    settings = get_settings()
    provider = create_llm_provider(settings)

    return AIEngine(provider=provider)
