# Phase 11: Dockerization & Orchestration Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-10 hours  

---

## 1. Executive Summary

This plan outlines the containerization and local orchestration architecture for the **AI Semantic Search Engine**. Designed for seamless local setup and environment parity, this phase containerizes our applications and orchestrates them into a unified multi-container system.

**Key Deliverables:**
- **Production-grade Dockerfiles** for the React frontend (multi-stage Nginx build) and FastAPI backend.
- **Docker Compose orchestrator** (`docker-compose.yml`) linking:
  - **Frontend:** React SPA exposed on port `5173`.
  - **Backend:** FastAPI API Gateway on port `8000`.
  - **Database:** PostgreSQL container with persistent storage volumes.
  - **Cache:** Redis key-value container.
- Core network boundaries and container startup health checks.

---

## 2. Pre-Implementation Verification & Setup

### Prerequisites
- Docker and Docker Compose installed on the host machine.
- All backend requirements listed inside `requirements.txt`.
- Frontend dependencies configured for standard production builds.

---

## 3. Deployment Topology & Compose Networking

```
                     ┌───────────────────────────┐
                     │     Docker Host Port      │
                     └──────┬─────────────┬──────┘
             Port 5173      │             │      Port 8000
                            ▼             ▼
               ┌────────────────┐     ┌────────────────┐
               │    Frontend    │     │    Backend     │
               │   Container    │     │   Container    │
               │    (Nginx)     │     │   (FastAPI)    │
               └────────┬───────┘     └───────┬────────┘
                        │                     │
                        ▼                     ▼
                ┌───────────────────────────────────────┐
                │          App Network (Bridge)         │
                └───────┬─────────────────────┬─────────┘
                        │                     │
                        ▼                     ▼
               ┌────────────────┐     ┌────────────────┐
               │   Postgres     │     │     Redis      │
               │   Container    │     │   Container    │
               └────────────────┘     └────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: FastAPI Backend Containerization
**Estimated Time:** 2.5 hours  
**Risk Level:** Medium  
**Files:** `backend/Dockerfile`

**Steps:**
1. Use a lightweight base image: `python:3.11-slim`.
2. Install compile dependencies (e.g., build tools required by FAISS or other scientific libraries).
3. Set the working directory to `/app`. Copy `requirements.txt` and install dependencies.
4. Copy application source code and expose port `8000`.
5. Define entrypoint using `uvicorn`:
   ```bash
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

**Success Criteria:**
- Image builds successfully and starts in isolation.
- App directory weights are optimized by utilizing multi-stage builds or deleting temporary packages.

---

### Task 2: React Frontend Containerization
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `frontend/Dockerfile`

**Steps:**
1. Multi-Stage Build Approach:
   - **Stage 1 (Build):** Use `node:20-slim`. Copy package details, install dependencies, copy codebase, and run `npm run build`.
   - **Stage 2 (Production):** Use `nginx:alpine`. Copy built SPA assets from Stage 1 into `/usr/share/nginx/html`.
2. Configure custom `nginx.conf` routing all fallback paths to `index.html` to support React Router single-page application routing.
3. Expose port `80` (mapped to `5173` in compose settings).

**Success Criteria:**
- Frontend container image compiles cleanly.
- SPA pages load without assets paths issues, and routing redirects correctly on refresh.

---

### Task 3: Docker Compose Configuration
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `docker-compose.yml`

**Steps:**
1. Declare service blocks: `db` (PostgreSQL), `redis` (Redis), `backend` (FastAPI), and `frontend` (React).
2. Wire container networking utilizing bridge mode.
3. Map persistent volumes:
   - PostgreSQL: `/var/lib/postgresql/data`.
   - FAISS Vectors: Persistent local path inside `/app/storage/`.
4. Configure environment variable values, password configs, and system secrets safely.
5. Set container boot sequencing dependencies using `depends_on` with `condition: service_healthy` checks.

**Success Criteria:**
- Running `docker-compose up --build -d` provisions all 4 services automatically.
- Database and Cache systems boot fully before backend API processes initialize.

---

### Task 4: Local Orchestration Health Verification
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `docker-compose.yml`

**Steps:**
1. Implement healthy checks:
   - Postgres: `pg_isready` check commands.
   - Backend: curl health endpoints (`/health`).
2. Add graceful shutdown behaviors inside compose scripts.

**Success Criteria:**
- Containers monitor execution status dynamically.
- System starts up gracefully with zero manual operations.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Run `docker-compose up -d`. Verify all containers show `Up` and `healthy` in `docker ps`.
- [ ] Open `http://localhost:5173` in a browser; sign in, upload a document, and verify that processing works correctly.
- [ ] Restart individual containers (e.g. `docker-compose restart backend`); check that connections are restored without data loss.

### Automated Tests
- Audit docker-compose config files using validation syntax commands (`docker-compose config`).
- Verify container logs show zero database or connection pool startup failures.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Data Persistence Failure** | Stopping containers accidentally drops local vector indices or PostgreSQL databases. | Map all data locations to persistent, host-managed Docker volumes. |
| **Medium: Architecture Mismatches** | FAISS or python-compiled libraries fail inside containers depending on host chip architectures (x86 vs ARM64/Apple Silicon). | Use highly-compatible base images and ensure compilation flags are setup correctly for multi-platform support. |
