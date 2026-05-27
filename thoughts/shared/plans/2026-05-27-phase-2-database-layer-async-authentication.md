# Phase 2: Database Layer & Async Authentication Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** Critical  
**Estimated Effort:** 10-14 hours  

---

## 1. Executive Summary

This plan outlines the design and implementation of the database foundation and secure async user authentication for the **AI Semantic Search Engine**. Following the concentric **4-Layer Onion Architecture** and standard **Pydantic Validation**, this phase establishes:
- The persistent database async engine and transaction boundaries.
- The `User` domain model and Repository pattern.
- A secure JWT-based authentication API (`/auth/register`, `/auth/login`, `/auth/me`).
- A Zustand-managed frontend auth store with Route Guards for protected pages.

**Key Benefits:**
- Concentric separation of domain layers from network interfaces.
- Safe asynchronous relational operations preventing blocking threads.
- Comprehensive request/response validation using strict Pydantic schemas.

---

## 2. Pre-Implementation Verification & Setup

### Prerequisites & Dependencies
- **Backend drivers:** `asyncpg` (PostgreSQL async dialect), `SQLAlchemy>=2.0.0`
- **Security:** `passlib[bcrypt]` or `argon2-cffi` for password hashing, `pyjwt` for JWT generation.
- **Frontend tools:** `zustand`, `axios`, `react-router-dom`.

### Database Connection Setup
Verify that local or containerized PostgreSQL is active and accessible via the database connection string:
`postgresql+asyncpg://user:password@localhost:5432/ai_search`

---

## 3. Onion Layer Architecture Mapping

When coding this phase, allocate files strictly inside the Concentric Onion boundaries:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/auth_router.py              │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/schemas/auth_schema.py      │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/domain/models/user.py                  │
│  - backend/src/domain/interfaces/user_repository.py    │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│  - backend/src/infrastructure/database/database.py    │
│  - backend/src/infrastructure/repositories/...        │
│  - backend/src/core/security/security.py              │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Async Database Context & Session Setup
**Estimated Time:** 1.5 hours  
**Risk Level:** Low  
**Files:** `backend/src/infrastructure/database/database.py`

**Steps:**
1. Configure the SQLAlchemy `create_async_engine` using settings loaded from `config.py`.
2. Configure `async_sessionmaker` with `autocommit=False`, `autoflush=False`, and `expire_on_commit=False`.
3. Provide an asynchronous session dependency injection provider `get_db_session()` using `yield` for route contexts.

**Success Criteria:**
- Relational database connections initialize cleanly.
- Async transaction boundaries execute without thread blocks.

---

### Task 2: User Domain Model & Repository Contract
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** 
- `backend/src/domain/models/user.py`
- `backend/src/domain/interfaces/user_repository.py`

**Steps:**
1. Define the `User` class inheriting from `Base` (SQLAlchemy 2.0 mapped types syntax).
2. Establish strict fields: `id` (UUID), `name`, `email`, `password_hash`, `created_at`, `updated_at`.
3. Define the abstract base class `IUserRepository` featuring abstract async operations: `get_by_id`, `get_by_email`, `create`.

**Success Criteria:**
- User entity model compiles cleanly with standard SQLAlchemy 2.0 type hints.
- Core Repository contract exposes only clean domain primitives.

---

### Task 3: Security & Cryptography Module
**Estimated Time:** 1.5 hours  
**Risk Level:** Medium  
**Files:** `backend/src/core/security/security.py`

**Steps:**
1. Establish a cryptographic wrapper utilizing `passlib` (with bcrypt backend) to securely hash and verify passwords.
2. Implement JWT token generators and parser functions utilizing `pyjwt`. Configure symmetric keys, expiries, algorithms (`HS256`).
3. Add a standard FastAPI dependency injection helper `get_current_user` to validate bearer tokens and extract session identities.

**Success Criteria:**
- Verification utilities securely hash passwords with modern salt factors.
- Expired or malformed tokens raise explicit HTTP 401 exceptions.

---

### Task 4: Use Cases & Validation Schemas
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:**
- `backend/src/application/schemas/auth_schema.py`
- `backend/src/application/services/auth_service.py`

**Steps:**
1. Code request models: `UserCreateRequest` (strict email verification), `UserLoginRequest`.
2. Code response models: `TokenResponse`, `UserResponse`.
3. Scaffold `AuthUseCase` coordinating registrations (checking if email exists, hashing passwords, creating rows) and logins.

**Success Criteria:**
- Invalid payloads trigger Pydantic validation errors before database transactions start.
- Auth orchestrator isolates transaction boundaries cleanly.

---

### Task 5: Authentication Routing (Presentation)
**Estimated Time:** 2 hours  
**Risk Level:** Medium  
**Files:** `backend/src/api/routes/auth_router.py`

**Steps:**
1. Implement `POST /auth/register` invoking the registration use-case.
2. Implement `POST /auth/login` returning tokens.
3. Implement `GET /auth/me` protected by `get_current_user` resolving active user state.

**Success Criteria:**
- REST endpoints return standardized payloads.
- Authentication responses don't leak relational fields or password hashes.

---

### Task 6: Zustand Authentication Store
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `frontend/src/stores/authStore.ts`

**Steps:**
1. Declare interface structures for `AuthState` (user entity, token, loading state, error states).
2. Wire up actions: `login`, `register`, `logout`, `fetchMe`.
3. Persist JWT token to local storage or cookies, updating Axios auth headers dynamically.

**Success Criteria:**
- Store handles async login states and tokens seamlessly.
- Page reloads preserve authenticated user identity.

---

### Task 7: Route Guards & Authenticated Views
**Estimated Time:** 1.5 hours  
**Risk Level:** Low  
**Files:** 
- `frontend/src/features/auth/components/LoginForm.tsx`
- `frontend/src/features/auth/components/RegisterForm.tsx`
- `frontend/src/components/guards/ProtectedRoute.tsx`

**Steps:**
1. Build highly-responsive glassmorphic input panels matching the theme tokens.
2. Code route wrapper `ProtectedRoute` evaluating active auth tokens; redirecting anonymous visitors to `/login`.
3. Connect screens to standard router navigation.

**Success Criteria:**
- Unauthenticated requests are redirected safely to the login screen.
- Layout displays clean feedback animations upon successful logins.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Registration: Post schema triggers Pydantic errors for malformed emails.
- [ ] Security: Password hash inside database is salted (does not match raw input).
- [ ] Authorization: Protected endpoints return HTTP 401 when called without a valid header.
- [ ] Frontend: Zustand auth state is populated correctly and persists across tab refreshes.

### Automated Tests Plan
Create async tests inside `backend/tests/api/test_auth.py` using `httpx.AsyncClient`:
- Test successful register.
- Test duplicate email rejection.
- Test invalid credential failures.
- Test `/auth/me` with mock session dependencies.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: SQL session leak** | Connections remain open on uncaught route errors, exhausting database pools. | Wrap sessions within standard `async with` blocks or secure FastAPI yield contexts. |
| **Medium: Authentication bypass** | Forged or invalid JWT tokens pass validation logic. | Use strong symmetric keys (`JWT_SECRET`) and strict signature validation checks. |
