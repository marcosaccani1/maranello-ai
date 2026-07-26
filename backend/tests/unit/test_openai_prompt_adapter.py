"""Unit tests for the OpenAI prompt adapter."""

import pytest

from app.ai.adapters import OpenAIPromptAdapter
from app.ai.prompts import (
    AssistantMessage,
    ContextMessage,
    Prompt,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


def test_adapt_combines_system_messages_into_instructions() -> None:
    """System messages should become a single instructions value."""
    prompt = Prompt(
        messages=(
            SystemMessage(content="Follow the application rules."),
            SystemMessage(content="Answer concisely."),
            UserMessage(content="Explain the warranty."),
        )
    )

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["instructions"] == (
        "Follow the application rules.\n\nAnswer concisely."
    )


def test_adapt_converts_user_message() -> None:
    """User messages should become OpenAI user input messages."""
    prompt = Prompt(messages=(UserMessage(content="Explain the warranty."),))

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["input"] == [
        {
            "role": "user",
            "content": "Explain the warranty.",
        }
    ]


def test_adapt_converts_assistant_message() -> None:
    """Assistant messages should preserve their assistant role."""
    prompt = Prompt(
        messages=(AssistantMessage(content="The warranty lasts 36 months."),)
    )

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["input"] == [
        {
            "role": "assistant",
            "content": "The warranty lasts 36 months.",
        }
    ]


def test_adapt_formats_context_message() -> None:
    """Context messages should become labelled user input."""
    prompt = Prompt(
        messages=(
            ContextMessage(
                content="The warranty lasts 36 months.",
                source="warranty-policy",
            ),
            UserMessage(content="How long is the warranty?"),
        )
    )

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["input"] == [
        {
            "role": "user",
            "content": (
                "Contextual information:\n"
                "Source: warranty-policy\n"
                "Content: The warranty lasts 36 months."
            ),
        },
        {
            "role": "user",
            "content": "How long is the warranty?",
        },
    ]


def test_adapt_uses_fallback_for_missing_context_source() -> None:
    """Context messages without a source should use a fallback label."""
    prompt = Prompt(messages=(ContextMessage(content="Available information."),))

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["input"][0]["content"] == (
        "Contextual information:\nSource: unspecified\nContent: Available information."
    )


def test_adapt_omits_instructions_when_no_system_message_exists() -> None:
    """The output should omit instructions when none are supplied."""
    prompt = Prompt(messages=(UserMessage(content="User request."),))

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert "instructions" not in result


def test_adapt_preserves_input_message_order() -> None:
    """Adapted messages should retain their original order."""
    prompt = Prompt(
        messages=(
            UserMessage(content="First question."),
            AssistantMessage(content="First answer."),
            UserMessage(content="Second question."),
        )
    )

    adapter = OpenAIPromptAdapter()

    result = adapter.adapt(prompt)

    assert result["input"] == [
        {"role": "user", "content": "First question."},
        {"role": "assistant", "content": "First answer."},
        {"role": "user", "content": "Second question."},
    ]


def test_adapt_rejects_tool_messages() -> None:
    """Tool messages should fail until tool adaptation is implemented."""
    prompt = Prompt(
        messages=(
            ToolMessage(
                content="Vehicle data retrieved.",
                tool_name="vehicle_database",
            ),
        )
    )

    adapter = OpenAIPromptAdapter()

    with pytest.raises(
        ValueError,
        match="Tool messages are not supported",
    ):
        adapter.adapt(prompt)
