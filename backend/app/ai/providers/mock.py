from time import perf_counter

from app.ai.models.response import AIResponse, TokenUsage
from app.ai.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Deterministic provider used during development and automated tests."""

    provider_name = "mock"

    def __init__(self, model: str = "mock-model") -> None:
        self._model = model

    def generate(self, message: str) -> AIResponse:
        """Return a predictable response without calling an external LLM."""

        start_time = perf_counter()

        content = (
            f'Maranello AI ha ricevuto correttamente il tuo messaggio: "{message}"'
        )

        latency_ms = (perf_counter() - start_time) * 1000

        return AIResponse(
            content=content,
            provider=self.provider_name,
            model=self._model,
            usage=TokenUsage(
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
            ),
            latency_ms=latency_ms,
            finish_reason="stop",
            metadata={
                "is_mock": True,
            },
        )
