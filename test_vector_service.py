import asyncio
from app.service.product_service import fetch_all_products
from app.service.vector_service import index_products, search_products

async def main() -> None:
    products = await fetch_all_products()
    print(f"Fetched {len(products)} products")
    
    indexed_count = index_products(products=products)
    print(f"Indexed {indexed_count} products")
    queries = [
        "comfortable footwear for running",
        "electronic devices and mobile accessories",
        "books for learning programming",
    ]

    for query in queries:
        print(f"\nQuery: {query}")

        results = search_products(query, n_results=5)

        for result in results:
            metadata = result["metadata"]

            print(
                f"- {metadata.get('name')} | "
                f"Category: {metadata.get('category')} | "
                f"Distance: {result['distance']:.4f}"
            )


if __name__ == "__main__":
    asyncio.run(main=main())
    
