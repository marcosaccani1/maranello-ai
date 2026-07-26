"""Builders used to create structured prompts."""

from collections.abc import Iterable

from app.ai.prompts.models import (
    ContextMessage,
    Prompt,
    SystemMessage,
    UserMessage,
)
from app.ai.prompts.templates import (
    DEFAULT_OUTPUT_INSTRUCTIONS,
    MARANELLO_SYSTEM_PROMPT,
)


class PromptBuilder:
    """Build structured prompts from user input and optional context."""

    def __init__(
        self,
        system_prompt: str = MARANELLO_SYSTEM_PROMPT,
        output_instructions: tuple[str, ...] = DEFAULT_OUTPUT_INSTRUCTIONS,
    ) -> None:
        """Initialize the prompt builder.

        Args:
            system_prompt: Default system instructions applied to prompts.
            output_instructions: Default response-generation instructions.
        """
        self._system_prompt = self._validate_text(
            system_prompt,
            field_name="system_prompt",
        )
        self._output_instructions = self._normalize_instructions(
            output_instructions,
        )

    def build(
        self,
        user_message: str,
        *,
        context: Iterable[ContextMessage] | None = None,
        system_prompt: str | None = None,
        output_instructions: Iterable[str] | None = None,
    ) -> Prompt:
        """Build a structured prompt.

        Args:
            user_message: Original message submitted by the user.
            context: Optional contextual messages available to the model.
            system_prompt: Optional system prompt override.
            output_instructions: Optional output instruction override.

        Returns:
            A validated and immutable Prompt instance.
        """
        resolved_system_prompt = (
            self._system_prompt
            if system_prompt is None
            else self._validate_text(
                system_prompt,
                field_name="system_prompt",
            )
        )

        resolved_output_instructions = (
            self._output_instructions
            if output_instructions is None
            else self._normalize_instructions(output_instructions)
        )

        messages = [
            SystemMessage(
                content=resolved_system_prompt,
                metadata={"category": "behavior"},
            )
        ]

        if resolved_output_instructions:
            messages.append(
                SystemMessage(
                    content=self._format_output_instructions(
                        resolved_output_instructions,
                    ),
                    metadata={"category": "output_instructions"},
                )
            )

        messages.extend(tuple(context or ()))

        messages.append(
            UserMessage(
                content=self._validate_text(
                    user_message,
                    field_name="user_message",
                )
            )
        )

        return Prompt(messages=tuple(messages))

    @staticmethod
    def _validate_text(value: str, *, field_name: str) -> str:
        """Validate and normalize a required textual value."""
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} must not be empty")

        return normalized_value

    @classmethod
    def _normalize_instructions(
        cls,
        instructions: Iterable[str],
    ) -> tuple[str, ...]:
        """Normalize a collection of output instructions."""
        return tuple(
            cls._validate_text(
                instruction,
                field_name="output_instruction",
            )
            for instruction in instructions
        )

    @staticmethod
    def _format_output_instructions(
        instructions: tuple[str, ...],
    ) -> str:
        """Format output instructions as a system-level message."""
        formatted_instructions = "\n".join(
            f"- {instruction}" for instruction in instructions
        )

        return f"Response requirements:\n{formatted_instructions}"
