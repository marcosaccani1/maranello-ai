from unittest.mock import Mock

from app.ai.engine import AIEngine
from app.ai.models.response import AIResponse
from app.ai.providers.base import BaseLLMProvider


def test_ai_engine_delegates_generation_to_provider() -> None:
    provider_response = AIResponse(
        content="Risposta generata",
        provider="mock",
        model="mock-model",
    )

    provider = Mock(spec=BaseLLMProvider)
    provider.generate.return_value = provider_response

    engine = AIEngine(provider=provider)

    response = engine.generate_response("Domanda di test")

    assert response == provider_response
    provider.generate.assert_called_once_with("Domanda di test")


def test_ai_engine_exposes_provider_name() -> None:
    provider = Mock(spec=BaseLLMProvider)
    engine = AIEngine(provider=provider)

    assert engine.provider_name == "Mock"