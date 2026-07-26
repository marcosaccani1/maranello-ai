import pytest
from pydantic import ValidationError

from app.ai.models.response import AIResponse, TokenUsage


def test_ai_response_contains_structured_generation_data() -> None:
    response = AIResponse(
        content="Risposta generata",
        provider="mock",
        model="mock-model",
        usage=TokenUsage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
        latency_ms=12.5,
        finish_reason="stop",
        metadata={"request_id": "test-request"},
    )

    assert response.content == "Risposta generata"
    assert response.provider == "mock"
    assert response.model == "mock-model"
    assert response.usage.input_tokens == 10
    assert response.usage.output_tokens == 5
    assert response.usage.total_tokens == 15
    assert response.latency_ms == 12.5
    assert response.finish_reason == "stop"
    assert response.metadata == {"request_id": "test-request"}


def test_ai_response_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        AIResponse(
            content="",
            provider="mock",
            model="mock-model",
        )


def test_token_usage_rejects_negative_values() -> None:
    with pytest.raises(ValidationError):
        TokenUsage(
            input_tokens=-1,
            output_tokens=0,
            total_tokens=0,
        )


def test_ai_response_is_immutable() -> None:
    response = AIResponse(
        content="Risposta generata",
        provider="mock",
        model="mock-model",
    )

    with pytest.raises(ValidationError):
        response.content = "Contenuto modificato"