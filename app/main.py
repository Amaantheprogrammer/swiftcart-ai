from dotenv import load_dotenv

load_dotenv()

import logging
import httpx
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from app.service.product_service import fetch_all_products, fetch_product_by_id, fetch_products
from app.service.vector_service import store_products
from app.router.chat_router import chat_router
from app.router.agent_router import agent_router
from app.util.env_util import (
    INDEX_STARTUP_RETRIES,
    INDEX_RETRY_DELAY,
    HTTP_READ_TIMEOUT,
    HTTP_CONNECTION_TIMEOUT
)
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level="INFO")
logger = logging.getLogger(name=__name__)

async def _seed_catalogue(client: httpx.AsyncClient) -> None:
    """
    Internal private helper
    Fetch all products from Springboot backend and store into ChromaDb
    """
    retries = INDEX_STARTUP_RETRIES
    delay = INDEX_RETRY_DELAY
    for i in range(1, retries + 1):
        try:
            logger.info("Fetching Swift Cart catalogue for vector indexing (attempt %s/%s)", i, retries)
            products = await fetch_all_products(client=client)
            indexed = await asyncio.to_thread(store_products, products)
            logger.info("Indexed %s products into Chroma", indexed)
            return
        except Exception:
            logger.exception("Catalogue indexing attempt %s failed", i)
            if i < retries:
                await asyncio.sleep(delay=delay * (2 ** (i - 1)))
    logger.error(msg="Catalogue indexing did not complete; product chat may be unavailable until indexed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = httpx.Timeout(
        timeout=HTTP_READ_TIMEOUT,
        connect=HTTP_CONNECTION_TIMEOUT,
    )
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        app.state.http_client = client
        # Keep indexing in the background so API startup/health checks are not blocked.
        seed_task = asyncio.create_task(_seed_catalogue(client), name="catalogue-indexing")
        app.state.seed_task = seed_task
        try:
            yield
        finally:
            seed_task.cancel()
            try:
                await seed_task
            except asyncio.CancelledError:
                pass

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


app.include_router(router=chat_router)
app.include_router(router=agent_router)

@app.get("/")
async def health_check():
    return {
        "success": True,
        "status": "UP",
        "service": "swift-cart-ai"
    }

@app.get("/products")
async def get_products(request: Request, page: int = 0, size: int = 20):
    try:
        products = await fetch_products(page, size, client=request.app.state.http_client)
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
async def get_product_by_id(request: Request, id: int):
    try:
        product = await fetch_product_by_id(id, client=request.app.state.http_client)
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
    
