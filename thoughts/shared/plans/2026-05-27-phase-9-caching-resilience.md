# Phase 9: Caching & Resilience Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-10 hours  

---

## 1. Executive Summary

This plan outlines the implementation of the caching and resilience layer for the **AI Semantic Search Engine**. To optimize response times, lower external API dependency costs, and build a fault-tolerant system, we will:
1. Integrate an asynchronous **Redis** caching database for frequent semantic search queries.
2. Implement robust API resilience wrappers (exponential backoff retries) around external LLM and embedding gateways to insulate the application from network hiccups or rate limits.

**Key Benefits:**
- Sub-millisecond retrieval speeds for highly repetitive search queries.
- Drastic reductions in LLM vendor API bills through intelligent caching.
- Clean degradation under vendor downtime, preventing cascading errors.

---

## 2. Pre-Implementation Verification & Setup

### Requirements & Drivers
- **Python Drivers:** `redis` (async-compatible Python Redis client), `tenacity` (retry library).
- **Relational Cache Configs:** Redis server initialized locally or inside a Docker container.
- **Key Parameters:** Configured `REDIS_URL`, `REDIS_CACHE_TTL_SECONDS` (default: 3600), and max connection pools.

---

## 3. Onion Layer Architecture Mapping

This resilience framework keeps cache configurations and vendor retry protocols strictly isolated:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/search_router.py            │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/services/cache_service.py │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│  - backend/src/infrastructure/cache/redis_client.py   │
│  - backend/src/infrastructure/external/embedding_...   │
│  - backend/src/infrastructure/external/llm_client.py   │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Asynchronous Redis Client Setup
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/infrastructure/cache/redis_client.py`

**Steps:**
1. Initialize async Redis client using `redis.asyncio.ConnectionPool.from_url`.
2. Wrap connection checks inside a startup lifecycle hook using a standard ping request.
3. Expose dependency injection provider `get_redis_client` with clean exception bounds.

**Success Criteria:**
- Redis client initializes cleanly.
- Sockets and connection pools close successfully when the FastAPI app shuts down.

---

### Task 2: Search Result Query Caching
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/cache_service.py`

**Steps:**
1. Code `CacheService` coordinating query key generation:
   - Generate SHA-256 hashes of standardized query inputs and parameters.
   - Format cache key structures: `search:cache:{user_uuid}:{query_hash}`.
2. Serialize JSON payloads matching output contracts cleanly.
3. Apply default 1-hour time-to-live (TTL) limits to cached data.

**Success Criteria:**
- Duplicate search queries bypass database and FAISS operations, resolving from Redis in under 5 milliseconds.
- Cached results represent exact representations of original output schemas.

---

### Task 3: API Resilience & Retry Wrappers
**Estimated Time:** 3 hours  
**Risk Level:** Low  
**Files:** 
- `backend/src/infrastructure/external/embedding_service.py`
- `backend/src/infrastructure/external/llm_client.py`

**Steps:**
1. Use the `tenacity` library to wrap external HTTP endpoints.
2. Implement exponential backoff:
   - Retry on standard rate limits (HTTP 429) or network timeouts.
   - Limit retries to 3 attempts with random jitter intervals.
3. Code graceful degradations (e.g. falling back to local sentence-transformers if external cloud APIs fail completely).

**Success Criteria:**
- Transient network dropouts recover automatically.
- Total connection failures degrade gracefully to fallback local systems.

---

### Task 4: Invalidation and Cache Purge Protocols
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/application/use_cases/ingest_document.py`

**Steps:**
1. Integrate cache eviction triggers inside document ingestion workflows.
2. Whenever a user uploads a new document, purge the user's cached search queries using wildcards: `search:cache:{user_uuid}:*`.
3. Provide an administrative endpoint `/api/cache/clear` protected by user credentials.

**Success Criteria:**
- Uploading fresh documents instantly evicts old search caches.
- Search queries immediately reflect new documents without manual cache clears.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Send a search request; verify the backend logs database and embedding operations.
- [ ] Resend the identical query; check that the backend handles the request without triggering DB or FAISS logs.
- [ ] Upload a new document; verify that the previous query now misses the cache and computes fresh results.

### Automated Tests
- Test Redis connection pooling under simulated network disconnects.
- Verify retry decorations using unit tests that intentionally return transient errors.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **Medium: Stale search cache** | Users search newly uploaded documents but see outdated cached results. | Evict all cache keys mapped to a user immediately when any ingestion completes. |
| **Low: Redis memory exhaustion** | High-volume query caches consume all available Redis RAM, causing crashes. | Enable standard Least-Recently-Used (`allkeys-lru`) eviction policies inside Redis server configurations. |
