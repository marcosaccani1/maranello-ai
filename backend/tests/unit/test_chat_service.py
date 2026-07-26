from unittest.mock import Mock

from app.ai.engine import AIEngine
from app.ai.models.response import AIResponse, TokenUsage
from app.services.chat_service import ChatService


def test_chat_service_uses_structured_ai_response() -> None:
    ai_response = AIResponse(
        content="Risposta dell'AI Engine",
        provider="mock",
        model="mock-model",
        usage=TokenUsage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
        latency_ms=20.0,
        finish_reason="stop",
    )

    ai_engine = Mock(spec=AIEngine)
    ai_engine.provider_name = "MockLLMProvider"
    ai_engine.generate_response.return_value = ai_response

    service = ChatService(ai_engine=ai_engine)

    response = service.ask("Domanda di test")

    assert response.answer == "Risposta dell'AI Engine"
    assert response.language == "it"
    assert response.sources == []

    ai_engine.generate_response.assert_called_once_with("Domanda di test")