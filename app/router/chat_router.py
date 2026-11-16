import logging

import httpx
from fastapi import APIRouter, HTTPException, Request

from app.schema.chat_schema import ChatRequest, ChatResponse
from app.service.chat_service import process_message

logger = logging.getLogger(name=__name__)
router = APIRouter(prefix="/ai", tags=["AI Chat"])


@router.post(path="/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    client: httpx.AsyncClient = http_request.app.state.http_client
    try:
        response = await process_message(message=request.message, client=client)
        return ChatResponse(response=response)
    except (httpx.HTTPError, ValueError) as e:
        logger.exception("Product discovery dependency failed")
        raise HTTPException(
            status_code=502,
            detail="Product discovery is temporarily unavailable. Please try again.",
        ) from e
    except Exception as e:
        logger.exception("Unexpected AI chat failure")
        raise HTTPException(
            status_code=503,
            detail="The AI assistant is temporarily unavailable. Please try again.",
        ) from e
