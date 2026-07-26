from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.ai.dependencies import get_ai_engine
from app.ai.engine import AIEngine
from app.ai.providers.mock import MockLLMProvider
from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Return an API client configured with the deterministic mock provider."""

    mock_engine = AIEngine(
        provider=MockLLMProvider(model="test-mock-model"),
    )

    app.dependency_overrides[get_ai_engine] = lambda: mock_engine

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_chat_returns_temporary_response(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Qual è la policy per il lavoro da remoto?",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload == {
        "answer": (
            "Maranello AI ha ricevuto correttamente il tuo messaggio: "
            '"Qual è la policy per il lavoro da remoto?"'
        ),
        "language": "it",
        "sources": [],
    }


def test_chat_rejects_empty_message(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": ""},
    )

    assert response.status_code == 422
