"""Unit tests for prompt domain models."""

import pytest
from pydantic import ValidationError

from app.ai.prompts.models import (
    AssistantMessage,
    ContextMessage,
    MessageRole,
    Prompt,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


def test_system_message_has_system_role() -> None:
    """A system message should expose the system role."""
    message = SystemMessage(content="Follow the application rules.")

    assert message.role == MessageRole.SYSTEM
    assert message.content == "Follow the application rules."


def test_user_message_has_user_role() -> None:
    """A user message should expose the user role."""
    message = UserMessage(content="Explain the warranty.")

    assert message.role == MessageRole.USER


def test_assistant_message_has_assistant_role() -> None:
    """An assistant message should expose the assistant role."""
    message = AssistantMessage(content="The warranty lasts 36 months.")

    assert message.role == MessageRole.ASSISTANT


def test_context_message_preserves_source_and_metadata() -> None:
    """A context message should preserve source information."""
    message = ContextMessage(
        content="The warranty lasts 36 months.",
        source="warranty-policy",
        metadata={"page": 8},
    )

    assert message.role == MessageRole.CONTEXT
    assert message.source == "warranty-policy"
    assert message.metadata == {"page": 8}


def test_tool_message_requires_tool_name() -> None:
    """A tool message should identify the tool that produced it."""
    message = ToolMessage(
        content="Vehicle information retrieved.",
        tool_name="vehicle_database",
    )

    assert message.role == MessageRole.TOOL
    assert message.tool_name == "vehicle_database"


def test_message_rejects_empty_content() -> None:
    """Prompt messages should reject empty content."""
    with pytest.raises(ValidationError):
        UserMessage(content="")


def test_tool_message_rejects_empty_tool_name() -> None:
    """Tool messages should reject an empty tool name."""
    with pytest.raises(ValidationError):
        ToolMessage(
            content="Tool result.",
            tool_name="",
        )


def test_prompt_preserves_message_order() -> None:
    """A prompt should preserve the order of its messages."""
    system_message = SystemMessage(content="System instructions.")
    user_message = UserMessage(content="User request.")

    prompt = Prompt(
        messages=(
            system_message,
            user_message,
        ),
    )

    assert prompt.messages == (
        system_message,
        user_message,
    )


def test_prompt_rejects_empty_message_collection() -> None:
    """A prompt should contain at least one message."""
    with pytest.raises(ValidationError):
        Prompt(messages=())


def test_prompt_is_immutable() -> None:
    """A constructed prompt should not be modified."""
    prompt = Prompt(
        messages=(UserMessage(content="User request."),),
    )

    with pytest.raises(ValidationError):
        prompt.messages = ()
