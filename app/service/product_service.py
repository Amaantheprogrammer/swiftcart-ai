import httpx
from dotenv import load_dotenv
from app.schema.product_schema import CreateProductRequest
from app.util.env_util import (
    PRODUCT_URL,
    HTTP_CONNECTION_TIMEOUT,
    HTTP_READ_TIMEOUT
)

load_dotenv()

def _timeout() -> httpx.Timeout:
    return httpx.Timeout(timeout=HTTP_READ_TIMEOUT, connect=HTTP_CONNECTION_TIMEOUT)

def _request_client(client: httpx.AsyncClient | None):
    """Use the app-wide pooled client, or a short-lived client for standalone use."""
    if client is not None:
        return client, False
    return httpx.AsyncClient(timeout=_timeout()), True

async def fetch_products(page: int = 0, size: int = 20, client: httpx.AsyncClient | None = None):
    http, owned = _request_client(client=client)
    try:
        response = await http.get(
            url=PRODUCT_URL,
            params={
                "page": page,
                "size": size
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["content"]
    finally:
        if owned:
            await http.aclose()

async def fetch_product_by_id(product_id: int, client: httpx.AsyncClient | None = None):
    http, owned = _request_client(client=client)
    try:
        response = await http.get(url=f"{PRODUCT_URL}/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    finally:
        if owned:
            await http.aclose()


async def fetch_all_products(size: int = 20, client: httpx.AsyncClient | None = None) -> list[dict]:
    http, owned = _request_client(client=client)
    try:
        all_products: list[dict] = []
        page = 0
        while True:
            response = await http.get(
                url=PRODUCT_URL,
                params={
                    "page": page,
                    "size": size
                }
            )

            response.raise_for_status()
            data = response.json()

            products = data["content"]
            all_products.extend(products)

            total_pages = data["totalPages"]

            if page + 1 >= total_pages:
                break

            page += 1

        return all_products
    finally:
        if owned:
            await http.aclose()
        

async def fetch_products_by_ids(product_ids: list[int], client: httpx.AsyncClient | None = None) -> list[dict]:
    if not product_ids:
        return []
    http, owned = _request_client(client)
    try:
        response = await http.post(
            url=f"{PRODUCT_URL}/batch",
            json={"productIds" : product_ids}
        )
        response.raise_for_status()
        return response.json()
    finally:
        if owned:
            await http.aclose()


async def create_product(request: CreateProductRequest, access_token: str, client: httpx.AsyncClient | None = None):
    http, owned = _request_client(client)
    try:
        response = await http.post(
            url=PRODUCT_URL,
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()
    finally:
        if owned:
            await http.aclose()
            
    """
    Git commit msg:
    Add product creation functionality and chat service enhancements
    - Implement CreateProductRequest schema for product creation.
    - Add create_product function to handle product creation logic.
    - Introduce create_product_agent for improved product discovery in chat.
    - Refactor process_message to utilize product agent for responses.
    """