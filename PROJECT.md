# Project: portfolio-ai-backend

## Architecture
- Backend RAG pipeline with modular FastAPI application architecture.
- Storage: Persistent local ChromaDB vector store (`chroma_db`).
- Embeddings: Ollama `nomic-embed-text`.
- LLM Generation: Ollama `llama3.2` with real-time Server-Sent Events (SSE) streaming.
- Constraints: Strict modularity; maximum 150 lines of code per Python file.

## Code Layout
- `app/__init__.py`: Package root
- `app/config.py`: Environment & configuration settings (<40 LOC)
- `app/models/chat.py`: Request/response Pydantic models (<30 LOC)
- `app/db/vectorstore.py`: Vector store connector & retrieval engine (<60 LOC)
- `app/services/document_loader.py`: Resume document loading & text chunking (<60 LOC)
- `app/services/ingest_service.py`: Ingestion service runner logic (<60 LOC)
- `app/services/rag_service.py`: RAG prompt construction & Ollama streaming generation (<90 LOC)
- `app/api/chat_router.py`: FastAPI chat router for `POST /chat` with SSE response (<70 LOC)
- `app/main.py`: FastAPI application entrypoint & middleware (<40 LOC)
- `ingest.py`: CLI script for triggering data ingestion (<30 LOC)
- `test_client.py`: Automated SSE streaming client test script (<60 LOC)

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| T1 | E2E Testing Suite | Requirements-driven E2E test harness & test cases | none | PLANNED |
| M1 | Ingestion & Vector DB Module | Modular ingest service, loader, vector store, ingest.py CLI | none | PLANNED |
| M2 | RAG & FastAPI SSE Streaming | RAG service, prompt template, chat router, FastAPI main app | M1 | PLANNED |
| M3 | Integration & Validation | End-to-end automated test script, Tier 1-5 tests, LOC check (<150) | T1, M2 | PLANNED |

## Interface Contracts
### Ingestion API
- `ingest_data(data_path: str, db_path: str) -> int`: Ingests document chunks into ChromaDB, returns chunk count.

### VectorStore API
- `get_vectorstore(db_path: str)`: Returns Chroma vector store instance.
- `get_retriever(db_path: str, k: int = 3)`: Returns retriever for top-k document chunks.

### RAG Service API
- `stream_chat_response(query: str) -> AsyncGenerator[str, None]`: Formats context from ChromaDB, calls Ollama `llama3.2`, yields SSE data formatted strings.

### FastAPI Chat Router
- `POST /chat`: JSON payload `{"query": "..."}` or `{"message": "..."}`. Returns `text/event-stream` SSE content.
