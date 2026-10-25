from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create the vector database
vector_store = Chroma(
    collection_name="swiftcart_products",
    embedding_function=embedding_model,
    persist_directory="./data/chroma-db",
)


# Convert product data into Document objects and store them in ChromaDB
def index_products(products: list[dict]) -> int:
    documents = []

    for product in products:
        product_id = product.get("id")

        if product_id is None:
            continue

        name = product.get("name") or ""
        category = product.get("categoryName") or ""
        price = product.get("price")
        description = product.get("description") or ""

        # Adjacent f-strings concatenate into one string.
        page_content = (
            f"Product: {name}\n"
            f"Category: {category}\n"
            f"Price: {price}\n"
            f"Description: {description}"
        )

        metadata = {
            "product_id": int(product_id),
            "name": str(name),
            "category": str(category),
        }

        if price is not None:
            metadata["price"] = float(price)

        documents.append(
            Document(
                page_content=page_content,
                metadata=metadata,
            )
        )

    if not documents:
        return 0

    # Re-indexing the same product IDs updates existing records.
    vector_store.add_documents(
        documents=documents,
        ids=[str(document.metadata["product_id"]) for document in documents],
    )

    return len(documents)


# Find products that are semantically similar to a query
def search_products(query: str, n_results: int = 5) -> list[dict]:
    if not query.strip() or n_results <= 0:
        return []

    results = vector_store.similarity_search_with_score(
        query,
        k=n_results,
    )

    return [
        {
            "document": document.page_content,
            "metadata": document.metadata,
            "distance": distance,
        }
        for document, distance in results
    ]

def retrieve_product_ids(query: str, n_results: int = 10, max_price: float | None = None) -> list[int]:
    if not query.strip() or n_results <= 0:
        return []

    metadata_filter = None
    if max_price is not None:
        metadata_filter = {"price": {"$lte": max_price}}

    results = vector_store.similarity_search(
        query,
        k=n_results,
        filter=metadata_filter,
    )

    return [
        document.metadata["product_id"]
        for document in results
        if document.metadata.get("product_id") is not None
    ]