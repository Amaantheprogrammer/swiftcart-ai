<div align="center">

# 🛒 Swift Cart AI

### An AI-powered shopping companion for intelligent product discovery.

**From natural-language shopping queries to semantically relevant product recommendations.**

Swift Cart AI is a catalogue-grounded AI service built with Python, FastAPI, LangChain, ChromaDB, and Google Gemini. It combines semantic vector search with authoritative commerce-backend data to help customers discover products through natural conversation.

<br/>

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Search-EF6C35?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM%20%2B%20Embeddings-8E75B2?style=for-the-badge)

<br/>

**Part of the Swift Cart ecosystem**

[Java Commerce Backend](https://github.com/Amaantheprogrammer/Swift-Cart-Backend-Project) ·
[Live Commerce API](https://e-commercebackendproject.onrender.com) ·
[Swagger Documentation](https://e-commercebackendproject.onrender.com/swagger-ui/index.html)

</div>

---

## 📌 Overview

Traditional product search often depends on exact keywords, product names, or predefined filters. Customers, however, usually describe what they need in natural language.

For example:

> "I need comfortable running shoes under ₹3,000."

**Swift Cart AI** makes product discovery conversational.

Instead of relying exclusively on keyword matching, the service:

1. Understands the customer's natural-language request.
2. Converts the query into an embedding.
3. Retrieves semantically relevant products from ChromaDB.
4. Fetches the corresponding product records from the Swift Cart commerce backend.
5. Applies supported constraints, such as maximum price and category.
6. Uses Google Gemini to generate a response grounded in the retrieved catalogue data.

The result is an AI shopping assistant that combines semantic relevance with structured product information.

### Project vision

The long-term goal is to evolve Swift Cart AI from a read-only product discovery assistant into a controlled, tool-using shopping agent.

Future capabilities may include cart management, wishlist operations, checkout assistance, order tracking, and confirmation-gated order placement.

> **Implementation status:** The current repository implements product discovery, product API proxy routes, semantic retrieval, and AI-generated recommendations. Cart mutations, wishlist operations, checkout, order placement, payment processing, and autonomous agent workflows are not implemented yet.

---

## ✨ Features

### Implemented

| Feature | Description |
|---|---|
| Natural-language shopping chat | Accepts conversational shopping requests through `POST /ai/chat`. |
| Semantic product search | Uses Google Gemini embeddings and ChromaDB to retrieve relevant products. |
| Persistent vector storage | Stores catalogue embeddings in a Chroma collection named `swiftcart_products`. |
| Catalogue ingestion | Fetches paginated product data from the Swift Cart backend. |
| Background indexing | Starts catalogue indexing without blocking FastAPI application startup. |
| Retry mechanism | Retries failed catalogue indexing attempts using exponential backoff. |
| Authoritative product lookup | Fetches current product records from the commerce backend after vector retrieval. |
| Price constraint extraction | Recognizes supported phrases such as "under", "below", "less than", and "maximum price". |
| Category filtering | Applies category matching against categories present in retrieved product candidates. |
| Grounded AI responses | Instructs Gemini to recommend only products supported by the supplied catalogue context. |
| Product API proxy | Exposes endpoints to list and retrieve products from the commerce backend. |
| Shared HTTP client | Reuses an application-wide asynchronous HTTPX client. |
| Interactive API documentation | Provides Swagger UI and ReDoc through FastAPI. |
| Configurable CORS | Allows requests from configured frontend origins. |

### Planned

- Hybrid semantic and keyword retrieval.
- Improved category and attribute filtering.
- Product reranking.
- Authenticated user context and JWT forwarding.
- LangGraph-based agent orchestration.
- Product comparison tools.
- Cart and wishlist management.
- Checkout preview and order placement.
- Order tracking and cancellation.
- Confirmation gates for consequential actions.
- User-scoped conversation state.
- Observability, tracing, and evaluation.

---

## 🏗️ Architecture

Swift Cart AI follows a retrieval-augmented generation (RAG) approach.

The vector database identifies relevant product candidates, while the commerce backend remains the authoritative source for product information.

```text
                     CUSTOMER
                        |
                        | Natural-language query
                        v
               FastAPI: POST /ai/chat
                        |
                        v
                   Chat Service
                        |
                        v
              Extract Supported Filters
                (e.g. maximum price)
                        |
                        v
              ChromaDB Similarity Search
                Google Gemini Embeddings
                        |
                        v
                Candidate Product IDs
                        |
                        v
              Swift Cart Commerce API
               Fetch Product Records
                        |
                        v
                Deterministic Filtering
                  Price / Category
                        |
                        v
                 Product Context
                        |
                        v
                Google Gemini LLM
                        |
                        v
              Natural-language Response
                        |
                        v
                     CUSTOMER
```

### Request lifecycle

**1. Catalogue ingestion**

During FastAPI lifespan startup, a background task attempts to fetch the complete product catalogue from the Swift Cart backend.

**2. Document preparation**

Each product is converted into a LangChain `Document` containing information such as:

- Product name
- Category
- Price
- Description
- Product ID in metadata

**3. Embedding generation**

Google Gemini embeddings convert the product documents into vector representations.

**4. Vector storage**

The generated embeddings are stored in ChromaDB under the `swiftcart_products` collection.

**5. Semantic retrieval**

When a customer submits a query, the service searches the vector collection for up to 10 semantically relevant candidates.

**6. Authoritative product lookup**

The retrieved product IDs are sent to the commerce backend through its batch product endpoint.

**7. Constraint filtering**

The service applies supported maximum-price and category constraints to the returned product records.

**8. Context construction**

The filtered product records are serialized into JSON and supplied as context to the language model.

**9. Response generation**

Google Gemini generates a natural-language response using the provided product context and grounding instructions.

### Why use both ChromaDB and the commerce backend?

ChromaDB is used for semantic retrieval, not as the source of truth for commerce information.

Product prices, stock, approval status, and other frequently changing attributes should be obtained from the commerce backend.

This separation helps prevent the assistant from relying exclusively on potentially stale vector metadata.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary application language |
| FastAPI | Asynchronous REST API framework |
| Uvicorn | ASGI application server |
| LangChain Core | Prompt templates and runnable composition |
| LangChain Google GenAI | Gemini chat and embedding integrations |
| Google Gemini | Language model and embedding generation |
| ChromaDB | Persistent vector database and similarity search |
| HTTPX | Asynchronous communication with the commerce backend |
| Pydantic | Request and response validation |
| python-dotenv | Environment variable configuration |

### AI and vector configuration

The application reads the following settings from environment variables:

| Setting | Purpose |
|---|---|
| `GEMINI_MODEL` | Google Gemini chat model |
| `EMBEDDING_MODEL` | Google Gemini embedding model |
| `GOOGLE_API_KEY` | Google AI API authentication |
| `SWIFTCART_BASE_URL` | Commerce backend base URL |

Additional operational settings:

| Setting | Purpose |
|---|---|
| `HTTP_READ_TIMEOUT` | HTTP read timeout |
| `HTTP_CONNECTION_TIMEOUT` | HTTP connection timeout |
| `INDEX_STARTUP_RETRIES` | Maximum catalogue indexing attempts |
| `INDEX_RETRY_DELAY` | Initial delay between indexing retries |

---

## 🗂️ Project Structure

```text
swiftcart-ai/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── router/
│   │   └── chat_router.py
│   │
│   ├── schema/
│   │   └── chat_schema.py
│   │
│   ├── service/
│   │   ├── chat_service.py
│   │   ├── product_service.py
│   │   └── vector_service.py
│   │
│   ├── util/
│   │   ├── env_util.py
│   │   ├── llm_util.py
│   │   └── product_util.py
│   │
│   └── test/
│       └── test_vector_service.py
│
├── data/
│   └── chroma-db/
│
├── requirements.txt
└── .gitignore
```

### Main modules

| Module | Responsibility |
|---|---|
| `main.py` | FastAPI application, lifespan management, background catalogue indexing, health and product routes |
| `chat_router.py` | Handles AI chat requests |
| `chat_schema.py` | Defines chat request and response schemas |
| `chat_service.py` | Coordinates semantic retrieval, product filtering, context construction, and LLM invocation |
| `product_service.py` | Handles asynchronous HTTP communication with the commerce backend |
| `vector_service.py` | Creates product documents, stores embeddings, and retrieves product candidates |
| `env_util.py` | Reads application configuration from environment variables |
| `llm_util.py` | Configures the Gemini chat model |
| `product_util.py` | Extracts supported shopping constraints and filters product records |

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.11 or newer.
- A Google AI API key with access to the configured Gemini models.
- Network access to the Swift Cart commerce backend.
- Git.

### 1. Clone the repository

```bash
git clone https://github.com/Amaantheprogrammer/swiftcart-ai.git

cd swiftcart-ai
```

Replace the repository URL if your AI repository uses a different name.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv

.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.11 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
# Google AI
GOOGLE_API_KEY=your_google_api_key

# Commerce backend
SWIFTCART_BASE_URL=https://e-commercebackendproject.onrender.com

# Gemini models
GEMINI_MODEL=your_supported_gemini_chat_model
EMBEDDING_MODEL=your_supported_gemini_embedding_model

# HTTP configuration
HTTP_READ_TIMEOUT=60
HTTP_CONNECTION_TIMEOUT=10

# Catalogue indexing
INDEX_STARTUP_RETRIES=3
INDEX_RETRY_DELAY=2
```

Use model identifiers supported by your Google AI account and the installed integration packages.

**Important configuration note:** The current `env_util.py` reads environment variables when the module is imported. Ensure `.env` is loaded before importing modules that depend on those settings. Loading dotenv afterward in `main.py` is too late for values already read during imports.

Never commit `.env`, API keys, access tokens, or production credentials.

### 5. Start the application

From the project root:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

The application starts its catalogue indexing task in the background.

The first indexing run may take longer because it needs to:

1. Fetch product pages from the commerce backend.
2. Convert product records into documents.
3. Generate embeddings.
4. Store the documents in ChromaDB.

The API can start while indexing is running, but AI product discovery may not work correctly until the catalogue has been indexed.

### 6. Access the application

| Resource | URL |
|---|---|
| Health check | http://localhost:8001/ |
| Product listing | http://localhost:8001/products?page=0&size=20 |
| Product details | http://localhost:8001/products/42 |
| AI chat | http://localhost:8001/ai/chat |
| Swagger UI | http://localhost:8001/docs |
| ReDoc | http://localhost:8001/redoc |
| OpenAPI schema | http://localhost:8001/openapi.json |

---

## 🔌 API Reference

### `GET /`

Returns the basic application health status.

**Example response**

```json
{
  "success": true,
  "status": "UP",
  "service": "swift-cart-ai"
}
```

This is an application-level health response. It does not currently guarantee that Gemini, ChromaDB, or the commerce backend is reachable.

### `GET /products`

Fetches a paginated product listing from the Swift Cart commerce backend.

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | Integer | `0` | Zero-based page number |
| `size` | Integer | `20` | Number of products requested |

**Example**

```http
GET /products?page=0&size=20
```

### `GET /products/{id}`

Retrieves a product using its numeric ID.

**Example**

```http
GET /products/42
```

Returns `404` if the requested product does not exist.

Upstream communication failures are translated into an HTTP `502` response.

### `POST /ai/chat`

Accepts a natural-language shopping request and returns an AI-generated response.

**Request**

```json
{
  "message": "Find comfortable running shoes under ₹3000"
}
```

**Response**

```json
{
  "response": "Here are some products that match your requirements..."
}
```

The response is dynamic and depends on the available catalogue, semantic retrieval results, supported filters, and language model output.

The request message must contain between 1 and 5,000 characters.

---

# 🧠 From RAG to Agentic Commerce

The next major evolution of Swift Cart AI is to move beyond read-only product discovery and introduce controlled commerce operations.

The objective is to build an assistant that can understand customer intent, select appropriate tools, execute authorized operations, and verify the results.

## Core design principle

> The LLM interprets intent. Application code validates it. The commerce backend authorizes and executes it.

The language model should never be treated as the authority for product prices, customer identity, permissions, order status, or transaction success.

## Proposed agent architecture

```text
                 CUSTOMER REQUEST
                        |
                        v
                Authentication
                        |
                        v
                 Intent Detection
                        |
                        v
                Entity Resolution
                        |
                        v
                  Tool Selection
                        |
                        v
                Argument Validation
                        |
                        v
                Execution Policy
                   /        \
                  /          \
             Read Tool     Write Tool
                 |              |
                 v              v
             Execute       Prepare Preview
                 |              |
                 |         Confirmation
                 |              |
                 |        Revalidate Data
                 |              |
                 |         Execute Action
                 |              |
                 +--------------+
                        |
                        v
                 Verify Result
                        |
                        v
               Generate Response
                        |
                        v
                     CUSTOMER
```

## Proposed tool modules

```text
app/
│
├── agent/
│   ├── graph.py
│   ├── state.py
│   └── policies.py
│
├── tools/
│   ├── product_tools.py
│   ├── cart_tools.py
│   ├── wishlist_tools.py
│   ├── order_tools.py
│   └── account_tools.py
│
├── clients/
│   └── swiftcart_client.py
│
├── schemas/
│   ├── tool_inputs.py
│   └── tool_outputs.py
│
└── services/
    ├── retrieval_service.py
    └── conversation_service.py
```

### 1. Product discovery tools

These should be the first tools introduced because they extend the existing RAG workflow without introducing transaction risks.

| Tool | Example customer request |
|---|---|
| `search_products` | Find wireless headphones under ₹2,000 |
| `get_product_details` | Tell me more about product 42 |
| `compare_products` | Compare products 42 and 51 |
| `list_categories` | Show available product categories |
| `check_product_availability` | Is product 42 in stock? |

### 2. Cart tools

| Tool | Example customer request |
|---|---|
| `get_cart` | Show my cart |
| `add_to_cart` | Add product 42 to my cart |
| `update_cart_item` | Change its quantity to 2 |
| `remove_from_cart` | Remove the headphones |
| `clear_cart` | Empty my cart |

### 3. Wishlist tools

| Tool | Example customer request |
|---|---|
| `get_wishlist` | Show my wishlist |
| `add_to_wishlist` | Save this product for later |
| `remove_from_wishlist` | Remove product 42 from my wishlist |

### 4. Order and checkout tools

| Tool | Example customer request |
|---|---|
| `preview_checkout` | Calculate my final order total |
| `place_order` | Place my order |
| `get_my_orders` | Show my recent orders |
| `get_order_status` | Where is order 123? |
| `cancel_order` | Cancel order 123 |

These are proposed tool contracts. Their corresponding commerce-backend endpoints must be verified before implementation.

## Transaction safety

Consequential operations require stricter controls than product searches.

For order placement, the recommended workflow is:

1. Retrieve the authenticated customer's cart.
2. Revalidate product availability and prices.
3. Calculate the final payable amount on the backend.
4. Present the exact order summary to the customer.
5. Obtain explicit confirmation.
6. Revalidate the checkout data before execution.
7. Submit the order with an idempotency key.
8. Verify the backend response.
9. Return the actual order ID and status.

Additional safeguards:

- Never trust a `userId` supplied by the LLM.
- Derive customer identity from the authenticated principal.
- Enforce authorization and ownership checks in the Java backend.
- Never store bearer tokens in vector documents or prompts.
- Prevent duplicate order placement during retries.
- Never claim an operation succeeded without backend confirmation.
- Do not let the LLM independently authorize or execute payments.

## Why LangGraph?

LangGraph is a planned addition for implementing explicit, stateful agent workflows.

It can help coordinate:

- Intent classification.
- Tool selection.
- Conditional routing.
- Confirmation checkpoints.
- Tool execution.
- Error handling.
- Result verification.

Although `langgraph` is included in the current dependency file, the current application does not yet implement a LangGraph workflow.

---

## 🔍 Engineering Improvements

The following areas are important next steps before treating the service as production-ready.

| Area | Current concern | Recommended improvement |
|---|---|---|
| Configuration | Environment variables are read during module import | Load and validate configuration before dependent modules initialize |
| Vector storage | The current Chroma initialization paths use different persistence configurations | Consolidate vector-store initialization and use one explicit persistence location |
| Indexing | Catalogue indexing is initiated during application startup | Introduce a dedicated indexing command or background worker |
| Incremental updates | Re-indexing does not explicitly handle deleted products | Add product update and deletion synchronization |
| Filtering | Category matching is limited to retrieved candidates | Resolve category intent independently and apply deterministic filtering |
| Retrieval | Semantic retrieval is the primary candidate selection mechanism | Introduce hybrid retrieval and reranking |
| API contracts | Batch product lookup depends on an upstream endpoint | Verify the endpoint contract and add integration tests |
| Dependencies | Requirements include packages not used by the current application | Separate runtime and development dependencies |
| Testing | Automated coverage is limited | Add unit, API, and integration tests |
| Observability | Limited request-level visibility | Add structured logs, correlation IDs, tracing, and metrics |
| Reliability | External model and backend dependencies can fail | Add bounded retries, dependency health checks, and graceful fallbacks |

### Suggested evaluation metrics

A useful AI application should be evaluated beyond whether its responses sound convincing.

| Metric | What it measures |
|---|---|
| Recall@K | Whether relevant products appear in retrieved candidates |
| Constraint accuracy | Whether recommended products satisfy hard user constraints |
| Grounded response rate | Whether product claims are supported by catalogue data |
| Tool success rate | Whether valid tool executions complete successfully |
| Confirmation compliance | Whether consequential actions require approval |
| Retrieval latency | Time spent retrieving product candidates |
| End-to-end latency | Total response time |
| Model cost | Token usage and external model costs |

---

## 🗺️ Roadmap

### Completed

- [x] FastAPI application setup
- [x] Health endpoint
- [x] Product listing proxy
- [x] Product detail proxy
- [x] Swift Cart catalogue ingestion
- [x] Product document preparation
- [x] Gemini embedding integration
- [x] ChromaDB vector storage
- [x] Semantic product retrieval
- [x] Gemini-powered product recommendations
- [x] Basic price extraction and filtering
- [x] Basic category matching
- [x] Background catalogue indexing
- [x] Shared asynchronous HTTP client

### Next milestones

- [ ] Consolidate environment configuration and vector-store initialization
- [ ] Verify commerce-backend integration contracts
- [ ] Add automated unit and integration tests
- [ ] Implement incremental catalogue synchronization
- [ ] Introduce hybrid search and reranking
- [ ] Improve structured product filtering
- [ ] Implement authenticated commerce API client
- [ ] Add read-only commerce tools
- [ ] Integrate LangGraph orchestration
- [ ] Implement cart and wishlist operations
- [ ] Add confirmation-gated checkout and order placement
- [ ] Introduce user-scoped conversation state
- [ ] Add tracing, evaluation, and production monitoring

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Implement your changes.
4. Add or update tests.
5. Verify the application locally.
6. Open a pull request describing the changes.

---

## 👨‍💻 Author

**Amaan Coatwala**

- GitHub: [@Amaantheprogrammer](https://github.com/Amaantheprogrammer)
- LinkedIn: [amaan-coatwala](https://www.linkedin.com/in/amaan-coatwala/)

---

<div align="center">

### Swift Cart AI

**Making product discovery conversational and building towards responsible agentic commerce.**

Built as the AI companion to the Swift Cart e-commerce platform.

</div>
