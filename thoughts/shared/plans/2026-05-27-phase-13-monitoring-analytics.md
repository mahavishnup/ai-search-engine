# Phase 13: Monitoring & Analytics Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-10 hours  

---

## 1. Executive Summary

This plan outlines the design and implementation of the monitoring, telemetry, and conversational analytics systems for the **AI Semantic Search Engine**. To ensure production reliability, optimize generation quality, and track user search patterns, this phase establishes:
1. An analytics collection database schema capturing user feedback (likes, dislikes, corrections).
2. Performance telemetry trackers (measuring vector match times, prompt assembly delays, and stream processing times) using standard metrics exports (Prometheus / Grafana).

**Key Benefits:**
- Data-driven prompt tuning through analysis of user feedback logs.
- Precise monitoring of system latency, highlighting slow external APIs.
- Production observability and automated alerts for system failures.

---

## 2. Pre-Implementation Verification & Setup

### Requirements & Drivers
- **Python Libraries:** `prometheus-client` (for exporting system telemetry).
- **Relational Analytics Setup:** Postgres database models mapping user logs.

---

## 3. Onion Layer Architecture Mapping

Observability interfaces and telemetry metrics hook cleanly into our concentric Onion layers:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/analytics_router.py          │
│  - backend/src/api/routes/metrics_router.py            │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/services/telemetry.py       │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/domain/models/feedback.py              │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Feedback Capture Database Schema
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `backend/src/domain/models/feedback.py`

**Steps:**
1. Define the `Feedback` SQLAlchemy model mapping user interactions: `id` (UUID), `search_history_id` (foreign key), `user_id` (foreign key), `rating` (`like` or `dislike`), `correction_text` (optional text field), and `created_at`.
2. Generate Alembic migration scripts to apply the new schema.
3. Code the `POST /api/analytics/feedback` API endpoint to persist user feedback.

**Success Criteria:**
- User interactions are captured and logged to the database.
- Feedback records link cleanly back to original query history nodes.

---

### Task 2: Core Telemetry & Performance Counters
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/telemetry.py`

**Steps:**
1. Configure Prometheus metric collectors:
   - **Histograms:** `rag_vector_search_duration_seconds` (tracks FAISS retrieval speeds), `rag_llm_stream_first_token_seconds` (time to first token).
   - **Counters:** `rag_queries_total` (total searches), `rag_failures_total` (failed runs), `rag_tokens_total` (tokens consumed).
2. Wire timing decorators into core search, embedding, and streaming services.

**Success Criteria:**
- Timing decorators log system statistics with microsecond precision.
- Prometheus counter instances compile without impacting retrieval performance.

---

### Task 3: Telemetry Export Endpoint (Metrics Gateway)
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/api/routes/metrics_router.py`

**Steps:**
1. Expose a secure, isolated REST endpoint `GET /api/metrics`.
2. Format exported data according to standard Prometheus text formats using `prometheus_client.generate_latest`.
3. Add IP-whitelisting middleware to restrict access to the metrics endpoint to monitoring services (like Prometheus scraper jobs).

**Success Criteria:**
- The metrics endpoint exports clean system telemetry.
- Security filters prevent public access to server performance details.

---

### Task 4: User Feedback React Components
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `frontend/src/features/search/components/FeedbackButtons.tsx`

**Steps:**
1. Design subtle interactive rating components (Thumbs Up / Thumbs Down icons) at the footer of each streaming answer card.
2. Animate states using hover effects: glowing neon green for likes, soft red for dislikes.
3. Open an optional input card on dislike clicks, enabling users to submit text corrections.

**Success Criteria:**
- Feedback buttons render cleanly at the bottom of streamed answers.
- Click events submit rating details asynchronously without interrupting active chats.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Run a search query, then click the Thumbs Up button; verify that the database feedback table creates a matching record.
- [ ] Navigate to `http://localhost:8000/api/metrics`; check that standard Prometheus metrics render in the browser.
- [ ] Simulate an API failure; confirm `rag_failures_total` counts increment immediately.

### Automated Tests
- Test database relations between history logs and feedback cards.
- Ensure that timing decorators export metrics safely even when telemetry databases are down.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **Medium: Telemetry Performance Drag** | Tracking system timings adds processing overhead to search queries. | Keep metrics operations in memory using fast lock-free primitive arrays. |
| **Low: Leakage via Metrics** | Deployed metrics endpoints expose sensitive search query details. | Limit metrics data strictly to numbers and durations. Never include query strings or user identities in metric logs. |
