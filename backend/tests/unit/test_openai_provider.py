from types import SimpleNamespace
from unittest.mock import Mock, patch

import httpx
import pytest
from openai import APIConnectionError

from app.ai.exceptions import (
    AIProviderConfigurationError,
    AIProviderRequestError,
)
from app.ai.providers.openai import OpenAIProvider


def test_openai_provider_requires_api_key() -> None:
    with pytest.raises(
        AIProviderConfigurationError,
        match="OPENAI_API_KEY is required",
    ):
        OpenAIProvider(
            api_key=None,
            model="test-model",
            timeout_seconds=30,
        )


@patch("app.ai.providers.openai.OpenAI")
def test_openai_provider_returns_structured_response(
    mock_openai_class: Mock,
) -> None:
    mock_client = Mock()
    mock_openai_class.return_value = mock_client

    mock_client.responses.create.return_value = SimpleNamespace(
        id="resp_test_123",
        output_text="Risposta OpenAI di test",
        usage=SimpleNamespace(
            input_tokens=12,
            output_tokens=8,
            total_tokens=20,
        ),
        output=[
            SimpleNamespace(
                status="completed",
            )
        ],
    )

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        timeout_seconds=30,
    )

    response = provider.generate("Domanda di test")

    assert response.content == "Risposta OpenAI di test"
    assert response.provider == "openai"
    assert response.model == "test-model"

    assert response.usage.input_tokens == 12
    assert response.usage.output_tokens == 8
    assert response.usage.total_tokens == 20

    assert response.latency_ms >= 0
    assert response.finish_reason == "completed"
    assert response.metadata == {
        "response_id": "resp_test_123",
    }

    mock_client.responses.create.assert_called_once_with(
        model="test-model",
        input="Domanda di test",
    )


@patch("app.ai.providers.openai.OpenAI")
def test_openai_provider_wraps_provider_errors(
    mock_openai_class: Mock,
) -> None:
    mock_client = Mock()
    mock_openai_class.return_value = mock_client

    request = httpx.Request(
        method="POST",
        url="https://api.openai.com/v1/responses",
    )

    mock_client.responses.create.side_effect = APIConnectionError(
        message="External provider error",
        request=request,
    )

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        timeout_seconds=30,
    )

    with pytest.raises(
        AIProviderRequestError,
        match="OpenAI could not generate a response",
    ):
        provider.generate("Domanda di test")
