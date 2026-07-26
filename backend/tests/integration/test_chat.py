from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_returns_temporary_response() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "Qual è la policy per il lavoro da remoto?"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["language"] == "it"
    assert payload["sources"] == []
    assert "Qual è la policy per il lavoro da remoto?" in payload["answer"]


def test_chat_rejects_empty_message() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": ""},
    )

    assert response.status_code == 422