# Phase 14: Advanced Improvements & Future Roadmap Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** Medium  
**Estimated Effort:** 12-16 hours  

---

## 1. Executive Summary

This plan outlines the roadmap and future architectural scaling routes for the **AI Semantic Search Engine**. As the system transitions to support enterprise-grade workloads, we will research and scaffold three next-generation RAG features:
1. **Hybrid Search Integration:** Combining semantic vector lookup (FAISS) with keyword searches (BM25) to optimize keyword precision.
2. **Similarity Reranking:** Integrating a reranker service (using a HuggingFace cross-encoder model or Cohere's Rerank API) to re-evaluate and rerank top-K matching chunks.
3. **Cloud Vector Migrations:** Designing distributed vector store adapters (migrating local FAISS to cloud services like Qdrant or Pinecone) to scale vector queries across production kubernetes clusters.

---

## 2. Pre-Implementation Verification & Setup

### Requirements
- Highly optimized RAG search engine active (Phases 5 & 6).
- Unified domain interfaces for semantic search services and embedding clients.

---

## 3. High-Level Future Scaling Topology

```
                  ┌─────────────────────────────────┐
                  │       Incoming Query            │
                  └────────┬────────────────┬───────┘
                           │                │
          Keyword (Lexical)│                │ Semantic (Vector)
                           ▼                ▼
                     ┌──────────┐      ┌──────────┐
                     │   BM25   │      │  Vector  │
                     │  Engine  │      │  Search  │
                     └────┬─────┘      └────┬─────┘
                          │                 │
                          ▼                 ▼
                     ┌────────────────────────────┐
                     │   Reciprocal Rank Fusion   │
                     │        (RRF) Merge         │
                     └──────────────┬─────────────┘
                                    │ (Top 25 Chunks)
                                    ▼
                     ┌────────────────────────────┐
                     │    Cross-Encoder Reranker  │
                     │  (HuggingFace or Cohere)   │
                     └──────────────┬─────────────┘
                                    │ (Top 5 highly-grounded Chunks)
                                    ▼
                     ┌────────────────────────────┐
                     │    Synthesis LLM Router    │
                     └────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Hybrid Search Adapter (Lexical + Vector)
**Estimated Time:** 4 hours  
**Risk Level:** Medium  
**Files:** `backend/src/infrastructure/database/hybrid_search.py`

**Steps:**
1. Integrate the `rank_bm25` library in python backend environment.
2. Index raw chunk texts inside a BM25 scoring model concurrently with the FAISS embedding updates.
3. Code the `HybridSearchProvider` running parallel searches:
   - Match query using lexical search (BM25).
   - Match query using semantic vector search (FAISS).
4. Combine rankings using Reciprocal Rank Fusion (RRF) scores.

**Success Criteria:**
- Query returns highly precise lexical search results matching names, codes, or exact terms.
- Hybrid rankings combine lexical search precision with vector search context.

---

### Task 2: Cross-Encoder Reranker Service
**Estimated Time:** 4 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/reranker.py`

**Steps:**
1. Define abstract `IReranker` contract interface.
2. Build `CrossEncoderReranker` supporting local processing or Cohere APIs:
   - Retrieve top-25 chunks using hybrid searches (Task 1).
   - Pass query and retrieved chunks through the reranker to calculate real relevance scores.
   - Sort chunks based on relevance scores and return only the top-5 chunks to the LLM.

**Success Criteria:**
- Reranking filters out weak semantic matches, sending highly relevant text chunks to the LLM prompt.
- Generation accuracy increases, and context-bloat costs decrease significantly.

---

### Task 3: Distributed Cloud Vector Stores (Qdrant or Pinecone)
**Estimated Time:** 5 hours  
**Risk Level:** High  
**Files:** `backend/src/infrastructure/database/qdrant_store.py`

**Steps:**
1. Define an abstract vector store interface: `IVectorStore`.
2. Build a concrete distributed cloud provider connector (e.g. Qdrant or Pinecone).
3. Implement batch upsert and payload storage methods (storing text chunk content and metadata directly inside the cloud vector index).
4. Implement metadata filtering queries in the cloud vector database to handle multiple users.

**Success Criteria:**
- Local FAISS indexes migrate successfully to cloud vector stores with zero changes to core business logic.
- Deployed vector stores support horizontal scaling and multi-tenant isolation out-of-the-box.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Run searches with specific keywords (e.g., precise file names or technical IDs); verify that hybrid search returns exact-match chunks at the top of the results.
- [ ] Log reranker scores; check that re-ordered results display higher relevance scores.
- [ ] Mock cloud vector client connection pools; confirm failover alerts trigger when services are unavailable.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Processing Latency** | Running BM25, vector search, and reranking sequentially adds major latency to queries. | Run lexical and vector queries in parallel using `asyncio.gather`. Set up lightweight, fast rerankers. |
| **Medium: Local HuggingFace Memory** | Deploying local deep learning models (like Cross-Encoders) requires high RAM and GPU memory. | Use lightweight, optimized models (e.g. `bge-reranker-base`) or delegate heavy workloads to external APIs (Cohere). |
