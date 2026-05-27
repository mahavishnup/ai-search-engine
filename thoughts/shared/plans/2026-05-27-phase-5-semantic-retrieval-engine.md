# Phase 5: Semantic Retrieval Engine Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-12 hours  

---

## 1. Executive Summary

This plan outlines the design and implementation of the semantic search and vector matching pipeline for the **AI Semantic Search Engine**. This phase serves as the bridge between raw mathematical similarity vectors and our relational chunk database. It provides high-speed similarity search, converts mathematical matches into structured, citation-ready context blocks, and exposes query interfaces to the client.

**Key Objectives:**
- Convert natural language queries into normalized embedding vectors.
- Query local FAISS indices using cosine similarity to retrieve the top-K matches.
- Query PostgreSQL asynchronously using matched chunk IDs to retrieve complete metadata.
- Expose `/api/search` endpoints returning detailed text nodes, confidence levels, and exact document references.

---

## 2. Pre-Implementation Verification & Setup

### Prerequisites
- Active FAISS Index Manager on disk (Phase 4).
- Database seeded with chunk rows (Phase 3).

### Vector Similarity Standard
Ensure vectors are normalized prior to FAISS lookup to guarantee cosine similarity values scale between `0.0` and `1.0`.

---

## 3. Onion Layer Architecture Mapping

The retrieval services are contained strictly within our concentric Onion structure:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/search_router.py            │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/services/search_service.py │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/domain/interfaces/search_contract.py   │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Search Service Interface
**Estimated Time:** 1.5 hours  
**Risk Level:** Low  
**Files:** `backend/src/domain/interfaces/search_contract.py`

**Steps:**
1. Declare the abstract base class `ISearchService`.
2. Define abstract async method `search(user_id: UUID, query: str, top_k: int = 5, filters: dict = None) -> list[ChunkMatch]`.
3. Declare `ChunkMatch` domain model encapsulating: `chunk_id`, `file_name`, `page_number`, `content`, and `similarity_score`.

**Success Criteria:**
- Search contracts cleanly define return schemas without network dependencies.
- Primitives compile with strict type validation.

---

### Task 2: Core Retrieval & Cosine Matcher
**Estimated Time:** 3.5 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/search_service.py`

**Steps:**
1. Implement class `SemanticSearchService` inheriting from `ISearchService`.
2. Core Search Logic:
   - Request embedding vector from `IEmbeddingProvider` for user query.
   - Normalize the returned vector to support Cosine similarity computations.
   - Execute query on `FAISSStoreManager` to fetch top-K indices and scores.
   - Extract matching database `chunk_uuid` keys using index mappings.
3. Database Metadata Hydration:
   - Query PostgreSQL async database using a `SELECT` query with `IN` clause to fetch target chunk text and parent document metadata.
   - Sort database rows matching the original FAISS similarity rank scores.

**Success Criteria:**
- Query executes without blocking FastAPI threads.
- Matched chunks map back to their parent document records.

---

### Task 3: REST API Gateway Route
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/api/routes/search_router.py`

**Steps:**
1. Define strict Pydantic validation schemas: `SearchRequest` (accepts user query string, limit K, and optional filters) and `SearchResponse`.
2. Implement route `POST /api/search` injecting database sessions and `ISearchService` dependency providers.
3. Validate user access, verify they own the matching files, and output standard JSON arrays.

**Success Criteria:**
- REST query interface rejects malformed schemas.
- JSON response payload returns structured citations.

---

### Task 4: Frontend Search Hook & Results Component
**Estimated Time:** 3 hours  
**Risk Level:** Low  
**Files:** 
- `frontend/src/features/search/hooks/useSearch.ts`
- `frontend/src/features/search/components/SearchResults.tsx`

**Steps:**
1. Write async query hook using TanStack React Query to fetch data from `/api/search`.
2. Build responsive results grid displaying:
   - Matching text snippets.
   - Expandable panels showing source document name, parent index, and page number coordinate.
   - Cosine similarity percentage badge indicators (styled with dynamic Tailwind classes).

**Success Criteria:**
- Component updates dynamically upon query submissions.
- Citations display transparent, clean user interaction paths.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Submit a natural language query; verify that returned JSON contains correct cosine similarity scores.
- [ ] Verify database logs show a single bulk async query instead of N sequential selects (prevent N+1).
- [ ] Test cross-user isolation: user A cannot search or match chunks belonging to user B.

### Automated Tests
- Test semantic search router with mock vector scores.
- Verify result sorting routines match FAISS output rankings.
- Ensure SQL queries return empty list cleanly when FAISS yields zero index matches.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Cross-Tenant Data Leak** | User searches match chunks belonging to other system users. | Enforce strict `user_id` query filters inside PostgreSQL select statements. |
| **Medium: Database N+1 queries** | Fetching chunk details executes individual SQL calls for each vector match. | Use bulk SQL `IN` selectors with eager relational joins on parent documents. |
