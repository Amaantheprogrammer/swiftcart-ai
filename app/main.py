import httpx
from fastapi import FastAPI, HTTPException
from app.service.product_service import fetch_product_by_id, fetch_products
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class ChatRequest(BaseModel):
    message: str


app = FastAPI(
    title="Swift Cart AI Service",
    description="AI-powered shopping assistant for Swift Cart",
    version="1.0.0"
)


@app.get("/")
async def health_check():
    return {
        "success": True,
        "status": "UP",
        "service": "swift-cart-ai"
    }


@app.get("/products")
async def get_products(page: int = 0, size: int = 20):
    try:
        products = await fetch_products(page, size)
        return {
            "count": len(products),
            "products": products
        }

    except (httpx.HTTPError, ValueError, KeyError) as e:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch products from Swift Cart backend."
        ) from e


@app.get("/products/{id}")
async def get_product_by_id(id: int):
    try:
        product = await fetch_product_by_id(id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {id} not found"
            )
        return product

    except HTTPException:
        raise

    except (httpx.HTTPError, ValueError) as e:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch product from Swift Cart backend."
        ) from e


@app.post("/ai/chat")
async def gemini_api_res(request: ChatRequest):
    model = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            temperature=0.4
        )
    response = await model.ainvoke(request.message)
    return {
        "response": response.content[0]["text"]
    }
    
