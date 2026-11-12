import httpx
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.service.product_service import fetch_all_products, fetch_product_by_id, fetch_products
from app.service.vector_service import store_products
from app.router.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(coro=background_seed_database()) # co-routine object
    yield

async def background_seed_database():
    await asyncio.sleep(delay=5.0)
    
    max_retries = 5
    delay = 3.0
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Background seeding: Fetching products (Attempt {attempt})...")
            products = await fetch_all_products()
            if products:
                count = store_products(products)
                print(f"Successfully indexed {count} products into ChromaDB in the background!")
                break
        except Exception as e:
            print(f"Seeding attempt {attempt} failed: {e}. Retrying in {delay}s...")
            await asyncio.sleep(delay)
            delay *= 2

app = FastAPI(
    title="Swift Cart AI Service",
    description="AI-powered shopping assistant for Swift Cart",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "https://swiftcart-app.vercel.app"
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)

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

    except (httpx.HTTPError, ValueError) as e:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch product from Swift Cart backend."
        ) from e
    
