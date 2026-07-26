from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/chat", tags=["Chat"])

ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    chat_service: ChatServiceDependency,
) -> ChatResponse:
    """Process a chat request through the application service."""

    return chat_service.ask(request.message)