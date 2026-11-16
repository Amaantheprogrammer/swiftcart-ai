from functools import lru_cache
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.util.env_util import GOOGLE_API_KEY, EMBEDDING_MODEL

embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

# Create the vector database
vector_db = Chroma(
    collection_name="swiftcart_products",
    embedding_function=embedding_model,
    persist_directory="swiftcart_products",
)

@lru_cache(maxsize=1)
def create_vector_db() -> Chroma:
    if not GOOGLE_API_KEY:
        raise RuntimeError("Google API key is required to initialize product embeddings")
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name="swiftcart_products",
        embedding_function=embeddings,
        persist_directory="swiftcart_products",
    )

def _to_document(product: dict) -> Document | None:
    """
    Internal private helper
    Converts product to document
    """
    product_id = product.get("id")
    if product_id is None:
        return None
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return None

    name = str(product.get("name", ""))
    category = str(product.get("categoryName", ""))
    description = str(product.get("description", ""))
    price = product.get("price")
    page_content = (
        f"Product: {name}\nCategory: {category}\n"
        f"Price: {price if price is not None else 'unknown'}\n"
        f"Description: {description}"
    )
    metadata = {
        "product_id": product_id,
        "name": name,
        "category": category,
    }
    if isinstance(price, (int, float)) and not isinstance(price, bool):
        metadata["price"] = float(price)
    return Document(page_content=page_content, metadata=metadata)

# Convert product data into Document objects and store them in ChromaDB
def store_products(products: list[dict]) -> int:
    documents = []

    for product in products:
        document = _to_document(product)
        if document is not None:
            documents.append(document)

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
        n_results=n_results,
        max_price=None
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