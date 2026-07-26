"""Unit tests for the prompt builder."""

import pytest

from app.ai.prompts import (
    DEFAULT_OUTPUT_INSTRUCTIONS,
    MARANELLO_SYSTEM_PROMPT,
    ContextMessage,
    PromptBuilder,
    SystemMessage,
    UserMessage,
)


def test_build_creates_ordered_default_messages() -> None:
    """The builder should create the expected default message sequence."""
    builder = PromptBuilder()

    prompt = builder.build("What services are available?")

    assert len(prompt.messages) == 3

    behavior_message = prompt.messages[0]
    instructions_message = prompt.messages[1]
    user_message = prompt.messages[2]

    assert isinstance(behavior_message, SystemMessage)
    assert behavior_message.content == MARANELLO_SYSTEM_PROMPT
    assert behavior_message.metadata == {"category": "behavior"}

    assert isinstance(instructions_message, SystemMessage)
    assert instructions_message.metadata == {"category": "output_instructions"}

    for instruction in DEFAULT_OUTPUT_INSTRUCTIONS:
        assert instruction in instructions_message.content

    assert isinstance(user_message, UserMessage)
    assert user_message.content == "What services are available?"


def test_build_strips_user_message_whitespace() -> None:
    """The builder should normalize surrounding user-message whitespace."""
    builder = PromptBuilder()

    prompt = builder.build("   Tell me about the warranty.   ")

    user_message = prompt.messages[-1]

    assert isinstance(user_message, UserMessage)
    assert user_message.content == "Tell me about the warranty."


def test_build_places_context_before_user_message() -> None:
    """Context messages should be inserted before the user message."""
    builder = PromptBuilder()
    context_message = ContextMessage(
        content="The warranty lasts 36 months.",
        source="warranty-policy",
        metadata={"page": 8},
    )

    prompt = builder.build(
        "How long is the warranty?",
        context=[context_message],
    )

    assert prompt.messages[-2] == context_message
    assert isinstance(prompt.messages[-1], UserMessage)


def test_build_accepts_system_prompt_override() -> None:
    """The builder should support a request-specific system prompt."""
    builder = PromptBuilder()

    prompt = builder.build(
        "Summarize this document.",
        system_prompt="You are a document summarization assistant.",
    )

    system_message = prompt.messages[0]

    assert isinstance(system_message, SystemMessage)
    assert system_message.content == "You are a document summarization assistant."


def test_build_accepts_output_instruction_override() -> None:
    """The builder should support request-specific output instructions."""
    builder = PromptBuilder()

    prompt = builder.build(
        "Summarize this document.",
        output_instructions=["Return exactly three bullet points."],
    )

    instructions_message = prompt.messages[1]

    assert isinstance(instructions_message, SystemMessage)
    assert instructions_message.content == (
        "Response requirements:\n- Return exactly three bullet points."
    )


def test_build_omits_instruction_message_when_instructions_are_empty() -> None:
    """The builder should omit output instructions when none are configured."""
    builder = PromptBuilder(output_instructions=())

    prompt = builder.build("Explain the policy.")

    assert len(prompt.messages) == 2
    assert isinstance(prompt.messages[0], SystemMessage)
    assert isinstance(prompt.messages[1], UserMessage)


def test_build_rejects_empty_user_message() -> None:
    """The builder should reject empty user messages."""
    builder = PromptBuilder()

    with pytest.raises(
        ValueError,
        match="user_message must not be empty",
    ):
        builder.build("   ")


def test_builder_rejects_empty_system_prompt() -> None:
    """The builder should reject an empty default system prompt."""
    with pytest.raises(
        ValueError,
        match="system_prompt must not be empty",
    ):
        PromptBuilder(system_prompt="   ")


def test_build_rejects_empty_output_instruction() -> None:
    """The builder should reject empty output instructions."""
    builder = PromptBuilder()

    with pytest.raises(
        ValueError,
        match="output_instruction must not be empty",
    ):
        builder.build(
            "Explain the policy.",
            output_instructions=["Valid instruction.", "   "],
        )
