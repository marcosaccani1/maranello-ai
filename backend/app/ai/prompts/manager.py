"""Application-facing prompt management service."""

from collections.abc import Iterable

from app.ai.prompts.builders import PromptBuilder
from app.ai.prompts.models import ContextMessage, Prompt


class PromptManager:
    """Coordinate prompt construction for application use cases."""

    def __init__(self, builder: PromptBuilder | None = None) -> None:
        """Initialize the prompt manager.

        Args:
            builder: Optional prompt builder dependency.
        """
        self._builder = builder or PromptBuilder()

    def create_chat_prompt(
        self,
        user_message: str,
        *,
        context: Iterable[ContextMessage] | None = None,
    ) -> Prompt:
        """Create a structured prompt for a chat request.

        Args:
            user_message: Message submitted by the user.
            context: Optional contextual messages available to the model.

        Returns:
            A validated structured prompt.
        """
        return self._builder.build(
            user_message=user_message,
            context=context,
        )
