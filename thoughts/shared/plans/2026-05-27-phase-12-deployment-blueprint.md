# Phase 12: Deployment Blueprint Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 8-10 hours  

---

## 1. Executive Summary

This plan outlines the production release blueprint and database migration architecture for the **AI Semantic Search Engine**. Tying together our containerized services, this phase provides deployment recipes, configures production-ready managed databases, and integrates **Alembic** to coordinate schema modifications safely.

**Key Components:**
- Production deployment steps:
  - **Frontend:** Serverless hosting (Vercel or Netlify) optimized for speed.
  - **Backend:** Managed container environments (Render, Railway, or AWS ECS).
- Production database integration using managed cloud clusters (Neon, Supabase) and Alembic migration workflows.
- Environment variables and security configurations.

---

## 2. Pre-Implementation Verification & Setup

### Database Configuration Prerequisite
Ensure that your database connection settings support SSL connections, which are required by most managed cloud database providers (e.g. Neon, Supabase).

### Alembic Inits
Install `alembic` in the backend python environment:
`pip install alembic`

---

## 3. Deployment Topology & Managed Cloud Architecture

```
                  ┌──────────────────────────────┐
                  │        User Browser          │
                  └──────┬────────────────┬──────┘
                         │                │
            HTTPS/Static │                │ HTTPS/SSE
                         ▼                ▼
             ┌────────────────┐     ┌────────────────┐
             │ Frontend Host  │     │  Backend Host  │
             │(Vercel/Netlify)│     │(Render/Railway)│
             └────────────────┘     └────────┬───────┘
                                             │
                   ┌─────────────────────────┼─────────────────────────┐
                   │                         │                         │
                   ▼ (SSL PG Connection)     ▼ (Local Disk / EFS)      ▼ (Secure API)
           ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
           │ Managed Cloud │         │  Persistent   │         │ External LLM  │
           │  PostgreSQL   │         │  Vector Disk  │         │  Gateway API  │
           └───────────────┘         └───────────────┘         └───────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Relational Schema Migrations with Alembic
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/alembic/`

**Steps:**
1. Initialize Alembic inside the backend root folder:
   ```bash
   alembic init alembic
   ```
2. Configure `alembic.ini` and edit `alembic/env.py` to:
   - Import our SQLAlchemy `Base` model metadata.
   - Enforce asynchronous database connection execution run loops.
3. Generate the initial baseline migration script:
   ```bash
   alembic revision --autogenerate -m "initial_schema"
   ```
4. Integrate auto-run migrations (`alembic upgrade head`) inside backend container startup scripts.

**Success Criteria:**
- Migration scripts generate clean, executable SQL.
- Deployments automatically execute schema updates safely on start.

---

### Task 2: Cloud Database Setup (Neon or Supabase)
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/core/config/config.py`

**Steps:**
1. Provision a serverless PostgreSQL instance on Neon or Supabase.
2. Update config parameters to require secure SSL database connections: `sslmode=require`.
3. Configure database pooling limits (`pool_size=10`, `max_overflow=20`) to manage serverless cloud connection limits.

**Success Criteria:**
- Backend establishes secure database connections to the cloud.
- Connection pools recycle cleanly under serverless scaling rules.

---

### Task 3: Backend & Vector Storage Deployment
**Estimated Time:** 3 hours  
**Risk Level:** High  
**Files:** `backend/render.yaml` or container configs

**Steps:**
1. Configure host settings on Render or Railway linking your GitHub repository.
2. Set up a **Persistent Volume Mount** (e.g. at `/app/storage/`) to save the persisted FAISS vector index files across application redeployments.
3. Inject production credentials and environment variables: `DATABASE_URL` (SSL), `REDIS_URL`, `JWT_SECRET`, and `LLM_API_KEY`.

**Success Criteria:**
- Backend builds and runs successfully in the production environment.
- Vector files persist across container restarts.

---

### Task 4: Frontend Static Deployment
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `frontend/vercel.json`

**Steps:**
1. Configure a new project on Vercel or Netlify pointing to `frontend/`.
2. Configure the production build command: `npm run build` and output folder `dist/`.
3. Inject the production API base URL: `env.VITE_API_URL` pointing to the deployed backend.
4. Set up Nginx-style rewrite fallback rules in `vercel.json` to handle React SPA router redirects.

**Success Criteria:**
- Frontend builds and deploys successfully to serverless hosting.
- Page routing and API requests function correctly in production.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Run a test deployment. Open the production website, register a new user, and verify database tables populate correctly.
- [ ] Upload a document, run a search query, and check that semantic streaming responses return successfully.
- [ ] Restart the backend container; verify that previously indexed document vectors remain active and searchable (confirming persistent volume storage is working).

### Automated Tests
- Run migration checks (`alembic check`) to verify schemas align perfectly.
- Confirm production SSL connections enforce encrypted transport layers.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Vector Index Loss** | Missing persistent volumes deletes the FAISS index on backend restarts, breaking semantic search. | Require persistent volumes and set up automated vector backups to cloud storage (e.g. AWS S3). |
| **Medium: Production Connection Spikes** | Serverless scaling exhausts Postgres database connections. | Configure strict connection pooling limits and use connection pooling proxies (like PgBouncer). |
