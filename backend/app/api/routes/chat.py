from typing import Annotated

from fastapi import APIRouter, Depends

from app.ai.dependencies import get_ai_engine
from app.ai.engine import AIEngine
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

AIEngineDependency = Annotated[AIEngine, Depends(get_ai_engine)]


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    ai_engine: AIEngineDependency,
) -> ChatResponse:
    """Process a chat request through the application service."""

    chat_service = ChatService(ai_engine=ai_engine)
    return chat_service.ask(request.message)