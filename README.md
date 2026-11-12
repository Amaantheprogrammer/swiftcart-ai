<div align="center">

# 🛒 Swift AI

### Your intelligent shopping companion — built for semantic product discovery today, agentic commerce tomorrow.

A catalogue-grounded AI service that understands natural-language shopping requests, retrieves relevant products using vector search, applies supported constraints, and generates helpful recommendations using Google Gemini.

<br/>

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=for-the-badge)
![Chroma](https://img.shields.io/badge/Chroma-Vector%20Database-EF6C35?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM%20%2B%20Embeddings-8E75B2?style=for-the-badge)

**Part of the Swift Cart ecosystem**

[Java Commerce Backend](https://github.com/Amaantheprogrammer/Swift-Cart-Backend-Project) ·
[Live Commerce API](https://e-commercebackendproject.onrender.com) ·
[Swagger Documentation](https://e-commercebackendproject.onrender.com/swagger-ui/index.html)

</div>

---

## 📌 Overview

Shopping catalogues can be large, and customers do not always know the exact product name or category they need. **Swift Cart AI** makes product discovery conversational.

A customer can describe a need in natural language — for example:

> “I need comfortable footwear for running under ₹3,000.”

The service uses semantic retrieval to find relevant products from the Swift Cart catalogue, retrieves the authoritative product records from the commerce backend, applies supported price/category constraints, and asks Gemini to generate a grounded response.

### The goal

Build a practical AI layer for an e-commerce platform that can grow from **read-only product discovery** into a **safe, tool-using shopping agent** capable of helping a signed-in customer manage a cart, wishlist, and orders with explicit authorization.

> **Scope and accuracy note:** The code in this repository currently implements product discovery and read-only product API routes. Cart modification, wishlist modification, checkout, order placement, payment, and autonomous agent workflows are proposed future integrations, they are not implemented features yet.

---

## ✨ Features

### Implemented in this repository

- **Natural-language shopping chat** through `POST /ai/chat`.
- **Semantic product retrieval** using Google Gemini embeddings and Chroma.
- **Persistent vector collection** named `swiftcart_products`.
- **Catalogue ingestion** by fetching paginated products from the Swift Cart backend.
- **Authoritative product lookup** after vector retrieval, so generated answers can use backend product records rather than vector text alone.
- **Maximum-price extraction** for supported phrases such as “under”, “below”, “less than”, “maximum price”, and “budget”.
- **Basic category matching** against categories present in the retrieved product candidates.
- **Grounded response instructions** that tell the model not to invent products, IDs, prices, or specifications.
- **Product API proxy routes** for listing and retrieving product details.
- **FastAPI interactive API documentation** through Swagger UI and ReDoc.
- **CORS configuration** for the configured frontend origins.

### Planned — not yet implemented

- Authenticated user context and JWT forwarding.
- Tool calling and multi-step agent orchestration with LangGraph.
- Cart and wishlist read/write operations.
- Checkout preview, order placement, and order tracking.
- Confirmation gates for consequential actions.
- User-scoped conversation state and preference memory.
- Tracing, evaluation, and production monitoring.

---

## 🧠 Architecture

```text
                         CUSTOMER
                            |
                            | Natural-language shopping query
                            v
                   FastAPI: POST /ai/chat
                            |
                            v
                      Chat Service
                            |
                  Extract supported filters
                   (e.g. maximum price)
                            |
                            v
                  Chroma Semantic Search
                   Gemini Embedding Model
                            |
                            v
                    Candidate Product IDs
                            |
                            v
                Swift Cart Commerce Backend
                  Fetch authoritative records
                            |
                            v
                  Price / Category Filtering
                            |
                            v
                  Grounded Product Context
                            |
                            v
                    Gemini Chat Model
                            |
                            v
                  Natural-language response
                            |
                            v
                         CUSTOMER
```

### Request lifecycle

1. **Catalogue loading:** During FastAPI lifespan startup, the service fetches product pages from the commerce backend.
2. **Document preparation:** Each product is converted into a LangChain `Document` containing its name, category, price, and description.
3. **Embedding and storage:** `GoogleGenerativeAIEmbeddings` generates vectors, which are stored in the Chroma collection `swiftcart_products`.
4. **Semantic retrieval:** The incoming message is searched against the vector collection. The current chat flow requests up to 10 candidate products.
5. **Backend lookup:** Retrieved product IDs are sent to the commerce backend's batch product endpoint.
6. **Constraint filtering:** The service applies a parsed maximum price and a category match when detected.
7. **Grounded generation:** The remaining product records are placed in the prompt context and Gemini generates the response under catalogue-grounding instructions.

**Why retrieve product details again?** The vector database is an index for finding candidates. It should not be treated as the authoritative source for live price, stock, approval, or other frequently changing commerce data.

---

## 🧰 Technology Stack

| Technology | Role |
|---|---|
| Python | Application language |
| FastAPI | HTTP API framework |
| Uvicorn | ASGI server |
| LangChain Core | Prompt templates and runnable composition |
| LangChain Google GenAI | Gemini chat and embedding integrations |
| Google Gemini | Language model and embedding model |
| ChromaDB | Persistent vector storage and similarity search |
| HTTPX | Asynchronous HTTP communication with the commerce backend |
| Pydantic | Request/response validation |
| python-dotenv | Local environment variable loading |

The source currently configures:
- Chat model: `gemini-3.5-flash-lite`
- Embedding model: `gemini-embedding-2`
- Chroma collection: `swiftcart_products`
- Chroma persistence path: `./data/chroma-db`

Model availability and naming can change by provider. Confirm that the model IDs are enabled for the Google AI account used to run the service.

---

## 🗂️ Project Structure

```text
swiftcart-ai/
│
├── app/
│   ├── main.py                     # FastAPI app, lifespan, health and product routes
│   │
│   ├── router/
│   │   └── chat.py                 # POST /ai/chat
│   │
│   ├── schema/
│   │   └── chat.py                 # ChatRequest and ChatResponse schemas
│   │
│   ├── service/
│   │   ├── chat_service.py         # Retrieval, filtering and LLM chain
│   │   ├── product_service.py      # HTTP calls to the commerce backend
│   │   └── vector_service.py       # Chroma indexing and retrieval
│   │
│   └── util/
│       ├── llm_util.py             # Gemini chat model configuration
│       └── product_util.py         # Price/category parsing and filtering
│
├── data/
│   └── chroma-db/                  # Local persistent vector database (generated)
│
├── test_vector_service.py          # Vector-service experiment script
├── requirements.txt                # Python dependencies
└── .gitignore
```

---

## ⚙️ Run Locally

### Prerequisites

- Python 3.11 or newer is a sensible starting point; use a version supported by the installed LangChain, Chroma, and Google GenAI packages.
- A Google AI API key with access to the configured Gemini chat and embedding models.
- Network access to the Swift Cart commerce backend.
- Git.

### 1. Clone the repository

```bash
git clone <YOUR_SWIFTCART_AI_REPOSITORY_URL>
cd swiftcart-ai
```

Replace the placeholder with the actual URL of this AI repository. The Java commerce backend is a separate project.

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

The current `requirements.txt` includes several integrations and libraries that are not imported by the current application flow. See the [Dependency cleanup](#-engineering-improvements-before-production) section before preparing a production deployment.

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_ai_api_key
```

The current source hardcodes the commerce backend base URL in `app/service/product_service.py`:

```python
SWIFTCART_BASE_URL = "https://e-commercebackendproject.onrender.com"
```

For a maintainable deployment, move this value into environment-based settings (for example, `SWIFTCART_BASE_URL`) and read it at application startup. Until that code change is made, adding the variable to `.env` alone will not change the URL used by the service.

**Never commit `.env`, API keys, access tokens, or production credentials.**

### 5. Start the FastAPI server

From the project root:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

On startup, the lifespan handler attempts to fetch all products and index them in Chroma. The first run may take longer because it needs to call the commerce API and generate embeddings.

### 6. Open the API documentation

| Resource | Local address |
|---|---|
| Health check | `http://localhost:8001/` |
| Product list | `http://localhost:8001/products?page=0&size=20` |
| Product details | `http://localhost:8001/products/{id}` |
| AI chat | `http://localhost:8001/ai/chat` |
| Swagger UI | `http://localhost:8001/docs` |
| ReDoc | `http://localhost:8001/redoc` |
| OpenAPI schema | `http://localhost:8001/openapi.json` |

---

## 🔌 API Reference

### `GET /`

Returns a basic service health response.

Example:
```json
{
  "success": true,
  "status": "UP",
  "service": "swift-cart-ai"
}
```

This is an application-level health response. It does not currently verify that Gemini, Chroma, or the commerce backend are all reachable.

### `GET /products`

Returns a page of products fetched from the commerce backend.

| Query parameter | Type | Default | Description |
|---|---:|---:|---|
| `page` | integer | `0` | Zero-based page number |
| `size` | integer | `20` | Number of products requested |

Example:
```http
GET /products?page=0&size=20
```

### `GET /products/{id}`

Fetches one product by its numeric ID.

Example:
```http
GET /products/42
```

Returns `404` when the upstream backend reports that the product does not exist.

### `POST /ai/chat`

Accepts a natural-language shopping query and returns an AI-generated response.

**Request**
```json
{
  "message": "Find comfortable running shoes under ₹3000"
}
```

**Response shape**
```json
{
  "response": "Here are the products that best match your request..."
}
```

The response content is dynamic and depends on the live catalogue, vector retrieval, supported filters, and model output. The sample response is illustrative.

---

# 🧭 Tool Integration Roadmap: From AI Chat to Agentic Commerce

The strongest next evolution is to turn Swift Cart AI into a **controlled shopping agent**. Rather than giving the language model unrestricted access to the backend, expose a set of small, typed tools. The model can choose an appropriate tool, while the AI service and Java backend validate every argument and enforce permissions.

## Design principle

> **The LLM interprets intent. Deterministic application code validates it. The commerce backend authorizes and executes it.**

This separation is critical for security, correctness, and recruiter-quality engineering.

## Phase 1 — Establish a clean tool architecture

Add dedicated modules instead of putting commerce operations directly inside `chat_service.py`.

```text
app/
├── agent/
│   ├── graph.py                    # LangGraph workflow and routing
│   ├── state.py                    # Typed state for each agent run
│   └── policies.py                 # Confirmation and execution policies
│
├── tools/
│   ├── product_tools.py            # Search, details, compare, availability
│   ├── cart_tools.py               # View and modify cart
│   ├── wishlist_tools.py           # View and modify wishlist
│   ├── order_tools.py               # Preview, place, track, cancel
│   └── account_tools.py             # Safe, authenticated account operations
│
├── clients/
│   └── swiftcart_client.py         # Shared HTTPX client and auth propagation
│
├── schemas/
│   ├── tool_inputs.py               # Strict Pydantic input schemas
│   └── tool_outputs.py              # Normalized tool result schemas
│
└── services/
    ├── retrieval_service.py         # Hybrid retrieval and filtering
    └── conversation_service.py      # Session and conversation handling
```

Each tool should have:
- One clearly defined responsibility.
- A strict Pydantic input schema.
- A normalized result schema.
- A timeout and bounded retry policy for network calls.
- Explicit read/write classification.
- Authorization checks in the backend.
- Structured errors that the agent can explain safely.

## Phase 2 — Integrate tools in a deliberate order

### A. Product discovery tools — build first

| Tool | Example request | Expected behaviour | Priority |
|---|---|---|---|
| `search_products` | “Find wireless headphones under ₹2,000” | Semantic retrieval plus exact filters | P0 |
| `get_product_details` | “Tell me more about product 42” | Fetch current product details | P0 |
| `compare_products` | “Compare products 42 and 51” | Compare verified catalogue attributes | P0 |
| `list_categories` | “Which categories are available?” | Fetch categories from backend | P1 |
| `check_product_availability` | “Is product 42 in stock?” | Fetch current inventory information | P0 |

**Why first?** These tools are low-risk, immediately useful, and improve the existing read-only assistant without requiring transaction permissions.

### B. Cart tools

| Tool | Example request | Expected behaviour | Priority |
|---|---|---|---|
| `get_cart` | “Show my cart” | Read the signed-in user's cart | P0 |
| `add_to_cart` | “Add product 42 to my cart” | Validate product and quantity, then add | P0 |
| `update_cart_item` | “Change the quantity to 2” | Update the correct cart line | P1 |
| `remove_from_cart` | “Remove the headphones” | Resolve the intended cart line and remove | P1 |
| `clear_cart` | “Empty my cart” | Clear the cart only after explicit confirmation | P2 |

### C. Wishlist tools

| Tool | Example request | Expected behaviour | Priority |
|---|---|---|---|
| `get_wishlist` | “Show my wishlist” | Read the signed-in user's wishlist | P1 |
| `add_to_wishlist` | “Save this product for later” | Add the selected product | P1 |
| `remove_from_wishlist` | “Remove product 42 from my wishlist” | Remove the selected product | P2 |

### D. Order and checkout tools

| Tool | Example request | Expected behaviour | Priority |
|---|---|---|---|
| `preview_checkout` | “What is my final total?” | Recalculate current cart and payable amount | P0 |
| `place_order` | “Place my order” | Place only after an explicit confirmation | P0 |
| `get_my_orders` | “Show my recent orders” | Fetch orders owned by the signed-in user | P1 |
| `get_order_status` | “Where is order 123?” | Fetch status after ownership validation | P1 |
| `cancel_order` | “Cancel order 123” | Check eligibility and require confirmation | P2 |

**P0** = first useful agent release; **P1** = next iteration; **P2** = later enhancement.

These are proposed tool contracts, not claims that matching endpoints already exist. Implement or verify each operation in the Java backend before exposing its tool. Do not invent backend routes based on the tool names.

## Phase 3 — Add LangGraph orchestration

`langgraph` is present in the current dependency file, but the uploaded source does not yet implement a LangGraph graph. Use it to make tool execution explicit and controllable.

```text
                 User request
                      |
                      v
             Authenticate session
                      |
                      v
             Understand the intent
                      |
                      v
             Select an allowed tool
                      |
                      v
             Validate tool arguments
                      |
                      v
             Is it a write action?
                 /          \
               No            Yes
               |              |
               v              v
         Execute read     Prepare preview
             tool               |
               |                v
               |          Ask for confirmation
               |                |
               |          Explicit approval?
               |             /      \
               |           No        Yes
               |           |          |
               |           v          v
               |          Stop    Revalidate data
               |                      |
               |                      v
               |                 Execute write
               |                      |
               +----------------------+
                              |
                              v
                     Verify backend result
                              |
                              v
                      Explain the outcome
```

Suggested graph nodes:
1. `authenticate_session`
2. `classify_intent`
3. `resolve_entities`
4. `select_tool`
5. `validate_arguments`
6. `request_confirmation`
7. `execute_tool`
8. `verify_result`
9. `format_response`

Keep the graph bounded: set a maximum number of tool calls per user turn, limit retries, and define a safe fallback when a tool fails or the model is uncertain.

## Phase 4 — Secure authentication and user isolation

Cart, wishlist, and order tools must operate on the currently authenticated customer.

Recommended flow:

1. The frontend sends the signed-in user's access token to the AI service over HTTPS.
2. The AI service validates the token or forwards it to the commerce backend's authenticated endpoints.
3. A shared HTTP client attaches the bearer token only to the intended backend request.
4. The Java backend derives the customer identity from the authenticated principal.
5. The backend checks ownership and role permissions for every operation.

Security rules:
- Never trust a `userId` generated by the LLM.
- Never let the model choose which user's cart or order to access.
- Never store access tokens in Chroma metadata, prompts, vector documents, or conversation memory.
- Never log passwords, bearer tokens, payment data, or unnecessary personal data.
- Enforce ownership and authorization in the Java backend, not only in the AI service.

## Phase 5 — Add confirmation and transaction safety

Not every tool call needs the same level of permission.

| Operation | Recommended policy |
|---|---|
| Search, compare, list categories | No confirmation |
| View cart, wishlist, or order history | No confirmation, but authentication required |
| Add an item to cart | Report the exact product and quantity; follow the frontend's confirmation policy |
| Remove a cart item | Confirm if the target is ambiguous |
| Clear the entire cart | Explicit confirmation |
| Add/remove wishlist item | Report the exact change |
| Preview checkout | No transaction; show the calculated summary |
| Place an order | **Always show the final order summary and require explicit confirmation** |
| Cancel an order | **Check eligibility and require explicit confirmation** |
| Payment or money movement | Separate secure backend authorization; never let the LLM authorize or execute payment by itself |

For order placement:
- Re-fetch product prices, stock, cart contents, and totals immediately before execution.
- Show the exact products, quantities, and final payable amount.
- Bind confirmation to that exact preview and expire it after a short period.
- Use an idempotency key to prevent duplicate orders on retries.
- Verify the backend result and return the real order ID and status.
- Never tell the customer that an order succeeded unless the backend confirms it.

## Phase 6 — Advanced features that make the project stand out

| Enhancement | Why it is valuable |
|---|---|
| Hybrid search | Combines semantic relevance with exact price/category/stock filters |
| Product reranking | Improves ordering of retrieved candidates |
| Conversational references | Understands “add the second one” or “compare it with the first” |
| User-approved preferences | Supports preferences such as budget or favourite categories |
| Order issue assistant | Explains order status and routes unsupported cases to human support |
| Human handoff | Safely handles payment failures and ambiguous requests |
| Tool-call audit trail | Makes agent actions traceable and debuggable |
| Evaluation dataset | Measures retrieval accuracy, constraint correctness, and tool success |
| Observability | Tracks latency, model calls, failures, and token usage |
| Rate limiting | Protects the API, model budget, and commerce backend |

### Suggested evaluation metrics

- **Retrieval Recall@K:** Are relevant products present in the retrieved candidates?
- **Constraint accuracy:** Does every recommended product satisfy the requested hard filters?
- **Grounded response rate:** Are product names, IDs, prices, and attributes supported by backend data?
- **Tool success rate:** Do valid tool calls complete successfully?
- **Confirmation compliance:** Are consequential actions blocked until the exact action is approved?
- **Latency and cost:** How long does each request take, and what is its model/API cost?

A small, version-controlled set of realistic shopping queries with expected products and constraints will make these improvements measurable.

---
## 🔍 Engineering Improvements Before Production

The following items are visible in the uploaded source snapshot and should be addressed before presenting the service as production-ready.

### 1. Make catalogue indexing reliable

The current FastAPI lifespan attempts a full catalogue fetch and indexing operation at every application startup. For production:
- Separate indexing from API startup.
- Add an explicit indexing/refresh command.
- Track the last successful indexing time.
- Upsert changed products and remove deleted product vectors.
- Avoid simultaneous full re-indexing by multiple application workers.
- Use a shared persistent vector store if the service is deployed with multiple instances.

### 2. Improve filtering correctness

Current price extraction supports a useful but limited set of phrases. Add tests for commas, decimals, currency symbols, upper/lower bounds, and ambiguous budgets.

Current category detection checks category names found in the retrieved candidates. This can miss a category that was not retrieved semantically. Resolve category intent against the full category list or a structured category classifier, then apply the category as a deterministic filter.

Also validate stock, approval status, and any other hard requirement against authoritative backend fields before recommending a product.

### 3. Clean up dependencies

The current `requirements.txt` includes a broad set of integrations and tools — including multiple model providers, FAISS, document parsers, pandas, Streamlit, and other packages — that are not imported by the current application flow.

For a leaner and more maintainable service:
- Keep only packages required by the active code.
- Separate runtime and development/test dependencies.
- Pin tested versions or use a lock file.
- Add test dependencies such as `pytest` and `pytest-asyncio` if using them.
- Remove integrations only after checking whether another module or deployment workflow uses them.

### 4. Add operational safeguards

- Configure explicit HTTP connect/read timeouts and bounded retries.
- Add structured logging and correlation IDs.
- Validate pagination inputs and cap maximum page sizes.
- Add API rate limiting and request-size limits.
- Restrict CORS to the actual frontend origins.
- Add readiness checks for dependencies separately from the basic liveness endpoint.
- Handle provider quota errors and backend downtime with clear, non-sensitive responses.

---

## 🗺️ Roadmap

- [x] FastAPI application and health endpoint
- [x] Product list and product detail proxy routes
- [x] Swift Cart catalogue ingestion
- [x] Product document creation and Chroma persistence
- [x] Gemini embedding-based semantic retrieval
- [x] Gemini-powered catalogue-grounded chat
- [x] Basic maximum-price and category filtering
- [ ] Fix source issues and align integration contracts
- [ ] Add automated unit, API, and integration tests
- [ ] Add environment-based settings and dependency lock
- [ ] Improve hybrid retrieval, filters, and reranking
- [ ] Add authenticated commerce API client
- [ ] Add read-only product, cart, wishlist, and order tools
- [ ] Add LangGraph orchestration and bounded tool execution
- [ ] Add confirmation-gated cart and order mutations
- [ ] Add user-scoped conversation state
- [ ] Add tracing, evaluation, and production monitoring

---

## 🤝 Contributing

Contributions, bug reports, and architecture suggestions are welcome.

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make a focused change and add tests.
4. Run the test suite and verify the API locally.
5. Open a pull request describing the change and its impact.

---

## 👨‍💻 Author

**Amaan Coatwala**

- GitHub: [@Amaantheprogrammer](https://github.com/Amaantheprogrammer)
- LinkedIn: [amaan-coatwala](https://www.linkedin.com/in/amaan-coatwala/)

---

<div align="center">

**Swift AI — From product discovery to responsible agentic shopping.**

Built as the AI companion to the Swift Cart e-commerce platform.

</div>
