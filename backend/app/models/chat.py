from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request payload accepted by the chat endpoint."""

    message: str = Field(
        min_length=1,
        max_length=4000,
        description="Message submitted by the user.",
    )


class ChatResponse(BaseModel):
    """Response payload returned by the chat endpoint."""

    answer: str
    language: str
    sources: list[str] = Field(default_factory=list)