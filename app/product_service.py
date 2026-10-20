import httpx

SWIFTCART_BASE_URL = "https://e-commercebackendproject.onrender.com"

async def fetch_products(page: int = 0, size: int = 20):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{SWIFTCART_BASE_URL}/products",
            params={"page": page, "size": size}
        )

        response.raise_for_status()

        data = response.json()
        return data["content"]


async def fetch_product_by_id(product_id: int):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{SWIFTCART_BASE_URL}/products/{product_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()
