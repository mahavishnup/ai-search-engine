# Phase 10: Optimization & Logging Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-10 hours  

---

## 1. Executive Summary

This plan outlines the optimization of the parsing and retrieval systems and the implementation of structured JSON logging for the **AI Semantic Search Engine**. Designed to scale gracefully under high-concurrency workloads, this phase targets:
1. Minimizing the RAM footprint during extraction of multi-page documents (releasing fitting buffers, explicit garbage sweeps).
2. Implementing structured JSON logging mapping critical transactions: request latency, FAISS similarity lookup times, and extraction delays.

**Key Benefits:**
- Significant reductions in system peak memory usage during large document ingestion.
- Production-ready logs that parse easily into log indexers (Elasticsearch, Logstash, Datadog).
- Granular performance profiling for every stage of the RAG pipeline.

---

## 2. Pre-Implementation Verification & Setup

### Requirements
- Complete relational models (Phase 2) and extraction pipelines (Phases 3 & 4).
- Logging standard library configured cleanly (we recently wired timed daily rotation inside `backend/src/core/logger/logger.py`).

---

## 3. Onion Layer Architecture Mapping

Performance monitoring and logging adapters cross-cut the application, but their configurations remain isolated:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/core/middleware/request_logging.py      │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/core/logger/logger.py                   │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│  - backend/src/infrastructure/database/database.py    │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Extraction Memory & Garbage Collection Optimization
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/parser_service.py`

**Steps:**
1. Refactor PDF extraction loop:
   - Load PDF documents inside context managers ensuring references are dropped instantly.
   - Force page-by-page rendering, releasing text blocks from memory immediately after extracting strings.
2. Call `gc.collect()` explicitly after processing large document streams.
3. Optimize sliding-window array storage allocations.

**Success Criteria:**
- Memory consumption profile scales linearly with page counts (rather than exponentially).
- Memory buffers release cleanly upon task completions.

---

### Task 2: Structured JSON Logging Framework
**Estimated Time:** 3 hours  
**Risk Level:** Low  
**Files:** `backend/src/core/logger/logger.py`

**Steps:**
1. Implement a custom JSON Formatter converting standard logging outputs to structured JSON strings.
2. Ensure log entries include unified transaction IDs (`correlation_id`), timestamps, log levels, messages, and key performance metrics (e.g. latency, query parameters).
3. Route errors, exceptions, and stack traces into JSON key-value blocks.

**Success Criteria:**
- Output log streams format as strict JSON objects.
- Third-party log collectors parse records without regex complications.

---

### Task 3: Performance Middleware (API Tracing)
**Estimated Time:** 2 hours  
**Risk Level:** Medium  
**Files:** `backend/src/core/middleware/request_logging.py`

**Steps:**
1. Code a custom Starlette middleware intercepting FastAPI requests.
2. Attach a unique `X-Correlation-ID` header to incoming requests.
3. Track request durations (using high-resolution timers) and log final stats: request method, URL path, response status, and processing latency.

**Success Criteria:**
- API request latencies are logged with microsecond precision.
- Correlation IDs map all nested logs produced during a single request context.

---

### Task 4: Ingestion Performance Profiling
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/application/use_cases/ingest_document.py`

**Steps:**
1. Instrument the ingestion pipeline with detailed timing hooks:
   - Log text extraction duration.
   - Log chunk database insert times.
   - Log embedding API response times.
   - Log FAISS index update times.
2. Package stats into unified structured logs: `{"event": "document_indexed", "doc_id": "...", "durations": {...}}`.

**Success Criteria:**
- Log trace displays exact bottlenecks in the ingestion process.
- Performance statistics enable data-driven tuning.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Run a document upload; verify logs contain precise duration stats for each stage of the pipeline.
- [ ] Send search queries; confirm the output console prints strict JSON format blocks.
- [ ] Trigger database errors; check that exceptions are logged with full stack traces in JSON format.

### Automated Tests
- Test JSON formatter yields valid JSON string.
- Assert request timing middleware intercepts and measures standard routes accurately.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Logging overhead** | Generating complex JSON strings on every query impacts performance under heavy workloads. | Only serialize complex logs for key events. Keep log levels set to `INFO` in production to filter out noisy `DEBUG` statements. |
| **Low: Log leakage** | JSON output leaks sensitive user information (passwords, JWT tokens). | Filter and sanitize sensitive key-value pairs (like `password`, `token`) inside the logging formatter. |
