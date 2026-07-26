from app.ai.providers.mock import MockLLMProvider


def test_mock_provider_returns_predictable_response() -> None:
    provider = MockLLMProvider()

    response = provider.generate("Messaggio di test")

    assert response == (
        'Maranello AI ha ricevuto correttamente il tuo messaggio: '
        '"Messaggio di test"'
    )