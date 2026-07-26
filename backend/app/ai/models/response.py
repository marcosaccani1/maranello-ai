from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TokenUsage(BaseModel):
    """Token consumption associated with an AI generation."""

    model_config = ConfigDict(frozen=True)

    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)


class AIResponse(BaseModel):
    """Provider-independent representation of an AI-generated response."""

    model_config = ConfigDict(frozen=True)

    content: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    usage: TokenUsage = Field(default_factory=TokenUsage)
    latency_ms: float = Field(default=0.0, ge=0.0)
    finish_reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
