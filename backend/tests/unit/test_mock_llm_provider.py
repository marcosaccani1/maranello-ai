from app.ai.providers.mock import MockLLMProvider


def test_mock_provider_returns_structured_response() -> None:
    provider = MockLLMProvider(model="test-model")

    response = provider.generate("Messaggio di test")

    assert response.content == (
        'Maranello AI ha ricevuto correttamente il tuo messaggio: "Messaggio di test"'
    )
    assert response.provider == "mock"
    assert response.model == "test-model"
    assert response.usage.input_tokens == 0
    assert response.usage.output_tokens == 0
    assert response.usage.total_tokens == 0
    assert response.latency_ms >= 0
    assert response.finish_reason == "stop"
    assert response.metadata == {"is_mock": True}
