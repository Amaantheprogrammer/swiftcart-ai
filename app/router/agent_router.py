import logging
import httpx

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.util.auth_util import get_access_token
from app.service.chat_service import create_action_agent
from app.schema.chat_schema import ChatRequest


logger = logging.getLogger(__name__)

agent_router = APIRouter(prefix="/agent", tags=["Agent Chat"])

@agent_router.post("/products")
async def action_chat(request: ChatRequest, access_token: str = Depends(get_access_token)):
    client: httpx.AsyncClient = request.app.state.http_client
    product_agent = create_action_agent(client=client, access_token=access_token)
    try:
        response = await product_agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        })

        messages = response["messages"]

        for msg in reversed(messages):
            if msg.type == "ai" and msg.content:

                return {
                    "success": True,
                    "response": msg.content
                }

        return {
            "success": False,
            "response": "I couldn't generate a response."
        }

    except Exception as e:

        logger.exception("Product action agent failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the requested operation."
        ) from e