"""Unit tests for the prompt manager."""

from unittest.mock import Mock

from app.ai.prompts import (
    ContextMessage,
    Prompt,
    PromptBuilder,
    PromptManager,
    SystemMessage,
    UserMessage,
)


def test_create_chat_prompt_uses_builder() -> None:
    """The manager should delegate prompt construction to the builder."""
    expected_prompt = Prompt(
        messages=(
            SystemMessage(content="System prompt."),
            UserMessage(content="User message."),
        )
    )

    builder = Mock(spec=PromptBuilder)
    builder.build.return_value = expected_prompt

    manager = PromptManager(builder=builder)

    result = manager.create_chat_prompt("User message.")

    builder.build.assert_called_once_with(
        user_message="User message.",
        context=None,
    )
    assert result == expected_prompt


def test_create_chat_prompt_forwards_context() -> None:
    """The manager should forward context messages to the builder."""
    context_message = ContextMessage(
        content="Available contextual information.",
        source="test-source",
    )

    expected_prompt = Prompt(
        messages=(
            SystemMessage(content="System prompt."),
            context_message,
            UserMessage(content="User message."),
        )
    )

    builder = Mock(spec=PromptBuilder)
    builder.build.return_value = expected_prompt

    manager = PromptManager(builder=builder)

    result = manager.create_chat_prompt(
        "User message.",
        context=[context_message],
    )

    builder.build.assert_called_once_with(
        user_message="User message.",
        context=[context_message],
    )
    assert result == expected_prompt


def test_create_chat_prompt_with_default_builder() -> None:
    """The manager should work with its default builder."""
    manager = PromptManager()

    prompt = manager.create_chat_prompt("Explain the available services.")

    assert prompt.messages
    assert isinstance(prompt.messages[0], SystemMessage)
    assert isinstance(prompt.messages[-1], UserMessage)
    assert prompt.messages[-1].content == "Explain the available services."
