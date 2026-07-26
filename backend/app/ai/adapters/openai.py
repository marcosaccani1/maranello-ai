"""Prompt adapter for the OpenAI Responses API."""

from typing import Literal, NotRequired, TypedDict

from app.ai.adapters.base import PromptAdapter
from app.ai.prompts.models import (
    AssistantMessage,
    ContextMessage,
    Prompt,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


class OpenAIInputMessage(TypedDict):
    """Text message accepted as input by the OpenAI Responses API."""

    role: Literal["user", "assistant"]
    content: str


class OpenAIPromptInput(TypedDict):
    """Provider-specific prompt representation for OpenAI."""

    input: list[OpenAIInputMessage]
    instructions: NotRequired[str]


class OpenAIPromptAdapter(PromptAdapter[OpenAIPromptInput]):
    """Convert domain prompts into OpenAI Responses API input."""

    def adapt(self, prompt: Prompt) -> OpenAIPromptInput:
        """Convert a structured prompt into OpenAI-compatible input.

        System messages are combined into the Responses API instructions
        field. User, assistant and context messages are converted into the
        ordered input sequence.

        Args:
            prompt: Provider-independent prompt domain model.

        Returns:
            OpenAI Responses API prompt input.

        Raises:
            ValueError: If the prompt contains an unsupported message type.
        """
        instructions: list[str] = []
        input_messages: list[OpenAIInputMessage] = []

        for message in prompt.messages:
            if isinstance(message, SystemMessage):
                instructions.append(message.content)
                continue

            if isinstance(message, UserMessage):
                input_messages.append(
                    {
                        "role": "user",
                        "content": message.content,
                    }
                )
                continue

            if isinstance(message, AssistantMessage):
                input_messages.append(
                    {
                        "role": "assistant",
                        "content": message.content,
                    }
                )
                continue

            if isinstance(message, ContextMessage):
                input_messages.append(
                    {
                        "role": "user",
                        "content": self._format_context_message(message),
                    }
                )
                continue

            if isinstance(message, ToolMessage):
                raise ValueError(
                    "Tool messages are not supported by the OpenAI prompt adapter yet"
                )

            raise ValueError(
                f"Unsupported prompt message type: {type(message).__name__}"
            )

        adapted_prompt: OpenAIPromptInput = {
            "input": input_messages,
        }

        if instructions:
            adapted_prompt["instructions"] = "\n\n".join(instructions)

        return adapted_prompt

    @staticmethod
    def _format_context_message(message: ContextMessage) -> str:
        """Format contextual information as an OpenAI user input message."""
        source_label = message.source or "unspecified"

        return (
            "Contextual information:\n"
            f"Source: {source_label}\n"
            f"Content: {message.content}"
        )
