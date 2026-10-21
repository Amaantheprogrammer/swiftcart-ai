from fastapi import APIRouter

from app.schema.chat import ChatRequest, ChatResponse
from app.service.chat_service import process_message

router = APIRouter(prefix="/ai", tags=["AI Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    response = await process_message(request.message)
    return ChatResponse(response=response)