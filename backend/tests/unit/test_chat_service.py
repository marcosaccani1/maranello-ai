from app.services.chat_service import ChatService


def test_chat_service_returns_temporary_response() -> None:
    service = ChatService()

    response = service.ask("Qual è la policy per il lavoro da remoto?")

    assert response.language == "it"
    assert response.sources == []
    assert "Qual è la policy per il lavoro da remoto?" in response.answer