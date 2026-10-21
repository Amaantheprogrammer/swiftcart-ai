import httpx

SWIFTCART_BASE_URL = (
    "https://e-commercebackendproject.onrender.com"
)


async def fetch_products(page: int = 0, size: int = 20):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{SWIFTCART_BASE_URL}/products",
            params={"page": page, "size": size}
        )
        response.raise_for_status()

        data = response.json()
        return data["content"]


async def fetch_product_by_id(product_id: int):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{SWIFTCART_BASE_URL}/products/{product_id}"
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()


async def fetch_all_products(size: int = 20):
    all_products = list[dict]
    page = 0

    async with httpx.AsyncClient(timeout=60.0) as client:
        while True:
            response = await client.get(
                f"{SWIFTCART_BASE_URL}/products",
                params={
                    "page": page,
                    "size": size
                }
            )

            response.raise_for_status()
            data = response.json()

            products = data["content"]
            all_products.extend(products)

            total_pages = data["page"]["totalPages"]

            if page + 1 >= total_pages:
                break

            page += 1

    return all_products

