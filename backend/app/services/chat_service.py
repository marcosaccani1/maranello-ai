from app.ai.engine import AIEngine
from app.models.chat import ChatResponse


class ChatService:
    """Application service responsible for handling chat requests."""

    def __init__(self, ai_engine: AIEngine) -> None:
        self._ai_engine = ai_engine

    def ask(self, message: str) -> ChatResponse:
        """Generate a response through the configured AI engine."""

        answer = self._ai_engine.generate_response(message)

        return ChatResponse(
            answer=answer,
            language="it",
            sources=[],
        )