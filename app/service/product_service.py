from fastapi import HTTPException

import httpx
import os

SWIFTCART_BASE_URL = os.getenv(key="SWIFTCART_BASE_URL")
PRODUCT_URL = f"{SWIFTCART_BASE_URL}/products"
DEFAULT_TIMEOUT = float(os.getenv(key="DEFAULT_TIMEOUT"))

async def fetch_products(page: int = 0, size: int = 20):
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(
            PRODUCT_URL,
            params={
                "page": page,
                "size": size
            }
        )
        response.raise_for_status()

        data = response.json()
        return data["content"]


async def fetch_product_by_id(product_id: int):
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(f"{PRODUCT_URL}/{product_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()


async def fetch_all_products(size: int = 20):
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        all_products: list[dict] = []
        page = 0

        while True:
            response = await client.get(
                PRODUCT_URL,
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

async def fetch_products_by_ids(product_ids: list[int]) -> list[dict]:
    if not product_ids:
        return []

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(
                url=f"{PRODUCT_URL}/batch",
                json={"productIds" : product_ids}
            )
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError, KeyError) as e:
        raise HTTPException(
            status_code=502,
            detail="Unable to batch-fetch products from Swift Cart backend."
        ) from e


