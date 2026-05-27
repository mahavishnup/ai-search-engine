# Phase 4: Vector Index & Persistent Storage Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** Critical  
**Estimated Effort:** 12-16 hours  

---

## 1. Executive Summary

This plan outlines the architecture and integration of the pluggable vector database and persistent embedding pipeline for the **AI Semantic Search Engine**. Designed with concentric **4-Layer Onion Boundaries** and configuration-driven modularity, this phase enables the translation of textual segments into high-dimensional vectors and their index storage.

Specifically, we support:
- **Pluggable Vector Stores:** Switch seamlessly between **FAISS** (local CPU flat index) and **Qdrant** (local or cloud cluster API) via the `.env` variable `VECTOR_DB_TYPE`.
- **Flexible Embedding Gateways:** Support local embeddings (`sentence-transformers`), cloud providers (Groq/OpenRouter), and local private servers like **LM Studio** (via OpenAI-compatible embedding calls at `http://localhost:1234/v1`).

---

## 2. Pre-Implementation Verification & Setup

### Required Libraries
- **Local Vector Engine:** `faiss-cpu` (for FAISS flat index).
- **Qdrant Client:** `qdrant-client` (async-compatible connector).
- **Local Embeddings:** `sentence-transformers` (for zero-cost local execution).
- **Async API Client:** `httpx` (for calling Groq, OpenRouter, and LM Studio).

### Blueprint Configurations (`.env`)
```ini
VECTOR_DB_TYPE=faiss  # Options: faiss | qdrant
EMBEDDING_PROVIDER=local  # Options: local | openai | groq | openrouter

# Base Coordinates
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=...
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

---

## 3. Onion Layer Architecture Mapping

All pluggable adapters are decoupled via Domain Interfaces:

```
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/use_cases/ingest_document.py│
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/domain/interfaces/embedding_provider.py │
│  - backend/src/domain/interfaces/vector_store.py       │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│  - backend/src/infrastructure/database/faiss_store.py  │
│  - backend/src/infrastructure/database/qdrant_store.py │
│  - backend/src/infrastructure/external/embedding_...   │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Decoupled Embedding & Vector Store Interfaces
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** 
- `backend/src/domain/interfaces/embedding_provider.py`
- `backend/src/domain/interfaces/vector_store.py`

**Steps:**
1. Define abstract base class `IEmbeddingProvider` with async methods `get_embedding(text: str)` and `get_embeddings(texts: list[str])`.
2. Define abstract base class `IVectorStore` exposing abstract async methods:
   - `upsert_vectors(document_id: UUID, vectors: list[list[float]], metadata: list[dict]) -> None`
   - `search_vectors(query_vector: list[float], top_k: int) -> list[VectorMatch]`
   - `delete_vectors(document_id: UUID) -> None`

**Success Criteria:**
- Core business use-cases are entirely isolated from the specific database engines or model providers.

---

### Task 2: Multi-Provider Embedding Service (Local, Cloud, LM Studio)
**Estimated Time:** 3.5 hours  
**Risk Level:** Medium  
**Files:** `backend/src/infrastructure/external/embedding_service.py`

**Steps:**
1. Implement `EmbeddingServiceProvider` inheriting from `IEmbeddingProvider`.
2. Wire config-driven branches based on `EMBEDDING_PROVIDER` inside `.env`:
   - **local**: Run local `sentence-transformers/all-MiniLM-L6-v2` queries in-memory.
   - **openai**: Call local **LM Studio** embedding routes (`POST /v1/embeddings`) with custom parameters.
   - **groq** / **openrouter**: Run cloud gateway requests using `httpx`.

**Success Criteria:**
- Provider abstracts translation schemas cleanly.
- Switching between local and cloud embedding endpoints requires only changing the `.env` file.

---

### Task 3: Pluggable Vector Store Concrete Implementations
**Estimated Time:** 5 hours  
**Risk Level:** High  
**Files:** 
- `backend/src/infrastructure/database/faiss_store.py`
- `backend/src/infrastructure/database/qdrant_store.py`

**Steps:**
1. Code `FAISSStore` implementing `IVectorStore`:
   - Keep a local thread-safe flat index persisted to storage volumes.
   - Map matching indexes to chunk UUIDs via standard serialization dictionaries.
2. Code `QdrantStore` implementing `IVectorStore`:
   - Connect asynchronously to Qdrant server coordinates.
   - Perform batch vector insertions and metadata payloads upserts directly.
   - Execute similarity searches utilizing Qdrant payload filters.
3. Code a dependency injection provider `get_vector_store` that reads `VECTOR_DB_TYPE` from `.env` to load the appropriate store.

**Success Criteria:**
- Use cases load and execute the target vector database dynamically depending on the `.env` variable.
- Operations yield identical return values regardless of the selected engine.

---

### Task 4: Ingestion & Vector Pipeline Orchestration
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/use_cases/ingest_document.py`

**Steps:**
1. Refactor `IngestDocumentUseCase` to inject abstract dependencies `IEmbeddingProvider` and `IVectorStore`.
2. Core Pipeline Execution:
   - Extract raw text coordinates page-by-page.
   - Slice text into recursive chunks (500 chars / 100 overlap).
   - Write relational rows to Postgres.
   - Request embeddings via the active provider.
   - Upsert vectors and metadata into the active vector store dynamically.

**Success Criteria:**
- Ingestion runs cleanly without relational session leakages.
- Documents populate both SQL tables and the target vector engine seamlessly.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Set `VECTOR_DB_TYPE=faiss` in `.env`; run a document upload; verify local FAISS files persist on disk.
- [ ] Spin up a Qdrant container, update `.env` to `VECTOR_DB_TYPE=qdrant`; upload another file; verify that vector counts populate correctly inside Qdrant panels.
- [ ] Set `EMBEDDING_PROVIDER=openai` and start **LM Studio** locally; run a search query and verify local logs capture the embedding requests.

### Automated Tests
- Mock both `IVectorStore` and `IEmbeddingProvider` interfaces to test use cases in isolation.
- Test FAISS persistence thread safety.
- Verify Qdrant connection lifecycles are managed properly.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Data Drift** | Mismatches between SQL chunk UUIDs and Vector database metadata maps. | Enforce strict primary key validations and transactions rollback on failures. |
| **Medium: Vendor lock-in** | Modifying DB structures breaks core query logic. | Ensure all vector operations pass exclusively through the abstract `IVectorStore` layer. |
