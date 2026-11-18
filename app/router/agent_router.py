import httpx

from app.util.auth_util import get_access_token

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)

from fastapi.security import (
    HTTPAuthorizationCredentials
)

from app.service.chat_service import create_action_agent

agent_router = APIRouter(prefix="/agent", tags=["Chat"])


@agent_router.post("/products")
async def action_chat(
    request: Request,
    message: str,
    credentials: HTTPAuthorizationCredentials = Depends(dependency=get_access_token)
):
    client: httpx.AsyncClient = (request.app.state.http_client)
    access_token = credentials.credentials
    product_agent = create_action_agent(
        client=client,
        access_token=access_token
    )
    try:
        response = await product_agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": message
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the requested operation."
        )