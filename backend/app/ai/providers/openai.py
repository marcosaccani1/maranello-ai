from time import perf_counter
from typing import Any

from openai import OpenAI, OpenAIError

from app.ai.exceptions import (
    AIProviderConfigurationError,
    AIProviderRequestError,
)
from app.ai.models.response import AIResponse, TokenUsage
from app.ai.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """LLM provider implemented through the OpenAI Responses API."""

    provider_name = "openai"

    def __init__(
        self,
        api_key: str | None,
        model: str,
        timeout_seconds: float,
    ) -> None:
        if not api_key:
            raise AIProviderConfigurationError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )

        self._model = model
        self._client = OpenAI(
            api_key=api_key,
            timeout=timeout_seconds,
        )

    def generate(self, message: str) -> AIResponse:
        """Generate a structured response through OpenAI."""

        start_time = perf_counter()

        try:
            response = self._client.responses.create(
                model=self._model,
                input=message,
            )
        except OpenAIError as exc:
            raise AIProviderRequestError(
                "OpenAI could not generate a response."
            ) from exc

        latency_ms = (perf_counter() - start_time) * 1000

        usage = self._extract_usage(response)
        finish_reason = self._extract_finish_reason(response)

        return AIResponse(
            content=response.output_text,
            provider=self.provider_name,
            model=self._model,
            usage=usage,
            latency_ms=latency_ms,
            finish_reason=finish_reason,
            metadata={
                "response_id": response.id,
            },
        )

    @staticmethod
    def _extract_usage(response: Any) -> TokenUsage:
        """Convert OpenAI usage information into the domain model."""

        usage = getattr(response, "usage", None)

        if usage is None:
            return TokenUsage()

        input_tokens = getattr(usage, "input_tokens", 0) or 0
        output_tokens = getattr(usage, "output_tokens", 0) or 0
        total_tokens = (
            getattr(
                usage,
                "total_tokens",
                input_tokens + output_tokens,
            )
            or 0
        )

        return TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

    @staticmethod
    def _extract_finish_reason(response: Any) -> str | None:
        """Extract a finish reason when exposed by the provider."""

        output = getattr(response, "output", None)

        if not output:
            return None

        status = getattr(output[-1], "status", None)

        if isinstance(status, str):
            return status

        return None
