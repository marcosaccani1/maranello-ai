from app.models.chat import ChatResponse


class ChatService:
    """Application service responsible for handling chat requests."""

    def ask(self, message: str) -> ChatResponse:
        """Generate a temporary response for the submitted message."""

        return ChatResponse(
            answer=(
                "Maranello AI ha ricevuto correttamente il tuo messaggio: "
                f'"{message}"'
            ),
            language="it",
            sources=[],
        )


def get_chat_service() -> ChatService:
    """Return the chat service instance."""

    return ChatService()