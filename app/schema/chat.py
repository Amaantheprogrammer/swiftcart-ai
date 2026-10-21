from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Customer's query to Swiftcart AI assistant"
    )

class ChatResponse(BaseModel):
    response: str