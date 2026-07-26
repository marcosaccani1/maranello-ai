import logging
from time import perf_counter

from app.ai.engine import AIEngine
from app.models.chat import ChatResponse

logger = logging.getLogger(__name__)


class ChatService:
    """Application service responsible for handling chat requests."""

    def __init__(self, ai_engine: AIEngine) -> None:
        self._ai_engine = ai_engine

    def ask(self, message: str) -> ChatResponse:
        """Generate a chat response through the configured AI engine."""

        start_time = perf_counter()

        logger.info(
            "Generating chat response with provider=%s",
            self._ai_engine.provider_name,
        )

        try:
            ai_response = self._ai_engine.generate_response(message)
        except Exception:
            logger.exception(
                "Chat response generation failed with provider=%s",
                self._ai_engine.provider_name,
            )
            raise

        service_latency_ms = (perf_counter() - start_time) * 1000

        logger.info(
            (
                "Chat response generated provider=%s model=%s "
                "provider_latency_ms=%.2f service_latency_ms=%.2f "
                "input_tokens=%d output_tokens=%d total_tokens=%d"
            ),
            ai_response.provider,
            ai_response.model,
            ai_response.latency_ms,
            service_latency_ms,
            ai_response.usage.input_tokens,
            ai_response.usage.output_tokens,
            ai_response.usage.total_tokens,
        )

        return ChatResponse(
            answer=ai_response.content,
            language="it",
            sources=[],
        )