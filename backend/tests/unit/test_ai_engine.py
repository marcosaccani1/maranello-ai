from unittest.mock import Mock

from app.ai.engine import AIEngine
from app.ai.providers.base import BaseLLMProvider


def test_ai_engine_delegates_generation_to_provider() -> None:
    provider = Mock(spec=BaseLLMProvider)
    provider.generate.return_value = "Risposta generata"

    engine = AIEngine(provider=provider)

    response = engine.generate_response("Domanda di test")

    assert response == "Risposta generata"
    provider.generate.assert_called_once_with("Domanda di test")