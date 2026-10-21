from app.service.llm_service import generate_response

async def process_message(message: str) -> str:
    response = await generate_response(message)
    return response