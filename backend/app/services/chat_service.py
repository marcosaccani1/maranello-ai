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
        """Generate a response through the configured AI engine."""

        start_time = perf_counter()

        logger.info(
            "Generating chat response with provider=%s",
            self._ai_engine.provider_name,
        )

        try:
            answer = self._ai_engine.generate_response(message)
        except Exception:
            logger.exception(
                "Chat response generation failed with provider=%s",
                self._ai_engine.provider_name,
            )
            raise

        elapsed_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Chat response generated with provider=%s elapsed_ms=%.2f",
            self._ai_engine.provider_name,
            elapsed_ms,
        )

        return ChatResponse(
            answer=answer,
            language="it",
            sources=[],
        )