from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

# Create the vector database
vector_db = Chroma(
    collection_name="swiftcart_products",
    embedding_function=embedding_model,
    persist_directory="./data/chroma-db",
)

# Convert product data into Document objects and store them in ChromaDB
def store_products(products: list[dict]) -> int:
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
    vector_db.add_documents(
        documents=documents,
        ids=[str(document.metadata["product_id"]) for document in documents],
    )

    return len(documents)


def _base_similarity_search(query: str, n_results: int, max_price: float | None):
    """
    Internal private helper: Handles query validation, metadata filters,
    and executes the vector search against ChromaDB.
    """
    if not query.strip() or n_results <= 0:
        return list()
    
    metadata_filter = {"price" : {"$lte" : max_price}} if max_price is not None else None
    
    return vector_db.similarity_search_with_score(
        query=query,
        k=n_results,
        filter=metadata_filter
    )
    
def search_products(query: str, n_results: int = 10):
    """
    Find products that are semantically similar to a query
    """
    search_result = _base_similarity_search(
        query=query,
        n_results=n_results
    )
    
    return [
        {
            "document" : document.page_content,
            "metadata" : document.metadata,
            "distance" : distance
        }
        for document, distance in search_result
    ]

def search_product_ids(query: str, n_results: int = 10, max_price: float | None = None) -> list[int]:
    """
    Retrieve productIds from ChromaDb with max price filter (for the chat pipeline)
    """
    results = _base_similarity_search(query, n_results=n_results, max_price=max_price)
    
    return [
        document.metadata["product_id"]
        for document, distance in results
        if document.metadata.get("product_id") is not None
    ]