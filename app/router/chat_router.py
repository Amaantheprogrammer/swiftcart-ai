import logging

import httpx
from fastapi import APIRouter, HTTPException, Request

from app.schema.chat_schema import ChatRequest, ChatResponse
from app.service.chat_service import process_message

from app.service.chat_service import create_rag_chain

logger = logging.getLogger(name=__name__)
chat_router = APIRouter(prefix="/ai", tags=["AI Chat"])

@chat_router.post("/chat")
async def product_chat(request: Request, message: str):
    client: httpx.AsyncClient = (
        request.app.state.http_client
    )

    rag_chain = create_rag_chain(client)

    try:
        response = await rag_chain.ainvoke({
            "message": message
        })

        return {
            "success": True,
            "response": response.content
        }

    except httpx.HTTPError:

        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve products from Swift Cart."
        )
