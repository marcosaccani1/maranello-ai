from unittest.mock import Mock

from app.ai.engine import AIEngine
from app.services.chat_service import ChatService


def test_chat_service_uses_ai_engine() -> None:
    ai_engine = Mock(spec=AIEngine)
    ai_engine.generate_response.return_value = "Risposta dell'AI Engine"

    service = ChatService(ai_engine=ai_engine)

    response = service.ask("Domanda di test")

    assert response.answer == "Risposta dell'AI Engine"
    assert response.language == "it"
    assert response.sources == []

    ai_engine.generate_response.assert_called_once_with("Domanda di test")