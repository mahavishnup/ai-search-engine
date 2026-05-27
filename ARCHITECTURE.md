# System Architecture Documentation — AI Semantic Search Engine

This document outlines the high-level architecture, directory layout, structural guidelines, and processing flows of the **AI Semantic Search Engine** project.

---

## 1. High-Level Design Overview

The system is designed as a modular, decoupled web application composed of:

1. **React Web Frontend (`frontend/`)**: A rich, responsive user interface built using modern React 19, Vite, TypeScript, Tailwind CSS, Zustand global state managers, Zod environment schemas, and TanStack React Query for cached REST transactions.
2. **FastAPI Backend Gateway (`backend/`)**: An enterprise-grade, asynchronous REST API gateway following **Onion/Clean Architecture** to ensure testability, component decoupling, and easy transition to separate microservices.
3. **Pluggable Vector Store (`local filesystem / cloud API`)**: Decoupled database engine supporting local flat indices using **FAISS** or cloud/local cluster databases using **Qdrant** (configurable dynamically via `.env`).
4. **PostgreSQL Relational DB (`postgres`)**: Relational database storage holding user details, file ingestion meta logs, matching text chunk blocks, and search audit history logs.


---

## 2. Directory Scaffolding & Scope

The unified project directory is structured as follows, with the role and meaning of each folder defined inline:

```text
ai-search-engine/
 ├── .claude/                       # Anthropic Claude specialized persona rules & guidelines
 ├── .gemini/                       # Google Gemini / Antigravity specialized developer guidelines & planning logs
 ├── .github/                       # Unified GitHub workflows, pull request templates, and modular rules
 │    ├── instructions/             # Core coding guidelines (endpoints creation, React structures, ORM rules)
 │    ├── prompts/                  # Large Language Model prompts library (testing, refactoring, formatting)
 │    ├── skills/                   # Packed capabilities (RAG indexing, backend Onion, React frontend tools)
 ├── backend/                       # FastAPI Backend Service (concentric 4-layer Onion architecture)
 │    ├── src/
 │    │    ├── api/                 # Presentation Layer: exposes controllers and handles HTTP boundaries
 │    │    │    ├── dependencies/   # Central dependencies injector (SQL sessions, JWT auth resolvers)
 │    │    │    ├── middleware/     # Core HTTP filters (CORS config, timing, correlation tracking)
 │    │    │    ├── routes/         # Standard REST routers grouped strictly by entity boundaries
 │    │    │    └── websocket/      # Async real-time communication modules
 │    │    ├── application/         # Application Layer: coordinates business workflows and orchestrates use-cases
 │    │    │    ├── constants/      # App-wide validation limits, bounds, and processing parameters
 │    │    │    ├── enums/          # Standard enum collections utilized across use-cases
 │    │    │    ├── schemas/        # Request/Response Pydantic schemas (Data Transfer Objects)
 │    │    │    └── services/       # Use-case business orchestrators (e.g. search and upload services)
 │    │    ├── core/                # System Level Foundations: handles server configurations and frameworks
 │    │    │    ├── config/         # Environment settings loaded via Pydantic BaseSettings
 │    │    │    ├── exceptions/     # Global custom exceptions and API validation error handlers
 │    │    │    ├── logger/         # JSON structured performance logs & daily timed rotation
 │    │    │    └── security/       # Cryptographic utilities, JWT tokens, and bcrypt pass hashing
 │    │    ├── domain/              # Domain Layer: core database models and storage contracts
 │    │    │    ├── models/         # ORM entities mapping Postgres database tables
 │    │    │    └── interfaces/     # Repository & vector store interfaces (decoupled contracts)
 │    │    ├── infrastructure/      # Infrastructure Layer: details database operations and framework bindings
 │    │    │    ├── database/       # DB session makers, connections pooling, and setup contexts
 │    │    │    ├── langchain/      # LangChain pipeline bindings & agents
 │    │    │    ├── llm/            # Model interfaces (NVIDIA, Groq, OpenRouter, LM Studio, Ollama)
 │    │    │    ├── mcp/            # Model Context Protocol endpoints
 │    │    │    ├── repositories/   # Concrete storage query modules implementing domain interfaces
 │    │    │    ├── utils/          # Platform helpers and specific algorithms
 │    │    │    └── vector/         # FAISS/Qdrant vector stores manipulation and similarity matches
 │    │    ├── shared/              # Shared helper modules across multiple layers
 │    │    │    └── helpers/        # General cross-cutting utilities
 │    │    ├── storage/             # Locally generated storage objects
 │    │    │    └── logs/           # Service runtimes logs directory
 │    │    ├── tests/               # Pytest automated test specifications (health checks, routers)
 │    │    └── main.py              # Application entry point: initializes FastAPI and binds core exception middleware
 ├── frontend/                      # Modern React Web App
 │    ├── public/                   # Static public assets (Vite served directly, e.g. icons, logos)
 │    ├── src/
 │    │    ├── api/                 # Axios clients and TanStack React Query cache definitions
 │    │    ├── assets/              # Local media files (icons, SVGs, images)
 │    │    ├── components/          # Standalone UI primitives (buttons, glowing boxes, modal inputs)
 │    │    ├── config/              # Setup variables (i18n, Zod environment schema config)
 │    │    ├── constants/           # Immutable global routes and application-wide limits
 │    │    ├── contexts/            # React providers sharing authentication and visual themes
 │    │    ├── enums/               # Client-side TypeScript enum definitions
 │    │    ├── env.ts               # Zod-validated environment config
 │    │    ├── features/            # Functional feature-driven modules (e.g. upload, search, auth)
 │    │    ├── hooks/               # Decoupled custom React state hooks (debounce, storage)
 │    │    ├── i18n/                # System multi-lingual catalogs & setups
 │    │    ├── layouts/             # Grid slot containers organizing page visual shells
 │    │    ├── lib/                 # Core bindings for Tailwind styles merger
 │    │    ├── pages/               # Functional pages rendering client navigation targets
 │    │    ├── routes/              # Client navigation paths and authenticated guardians
 │    │    ├── schemas/             # Form input validated structures using Zod
 │    │    ├── services/            # Client business logic and network adaptors
 │    │    ├── stores/              # React global states using Zustand stores
 │    │    ├── styles/              # Visual variables and Tailwind CSS utility configs
 │    │    ├── tests/               # Vitest unit and integration test suites
 │    │    ├── types/               # Type-safe model contracts and interfaces
 │    │    ├── utils/               # Text parsers, date calculations, value helpers
 │    │    ├── app.tsx              # Main App React component organizing screen layouts
 │    │    └── main.tsx             # DOM mount entry point loading React application and assets
 └── thoughts/                      # Shared workspace design plans, logic logs, and architecture iterations
      └── shared/
           └── plans/               # Chronological plans tracking each phase of development (Phases 1-14)
```

---

## 3. Scaffolding & Responsibilities (Folder Meanings)

To maintain absolute modularity and system clean boundaries, every folder in the workspace holds a precise architectural meaning:

### 3.1 Root Workspace Directories
- **`.claude/`**: Anthropic Claude specialized personas guidelines and workspace loader files.
- **`.gemini/`**: Google Gemini/Antigravity specialized developer guidelines, architectural safeguards, and master plans.
- **`.github/`**: Houses global developer guidelines (`instructions/`), reusable LLM instructions prompts (`prompts/`), packaged capabilities (`skills/`), and pull request verification checklists.
- **`backend/`**: Deployed server framework compiling FastAPI async presentation rules and transactional schemas.
- **`frontend/`**: Vite static compiler hosting modern React 19 SPA client layouts, public static files, and state management stores.
- **`thoughts/`**: Stores design planning plans, multi-phase engineering checklists (Phases 1-14), architectural design decisions, and system logs.

---

### 3.2 Backend Onion Layer Responsibilities
The backend rigorously isolates concerns into concentric boundaries:

```text
 ┌─────────────────────────────────────────────────────────┐
 │                       API Layer                         │
 │  - FastAPI controllers, request/response models         │
 ├─────────────────────────────────────────────────────────┤
 │                   Application Layer                     │
 │  - Business use cases, orchestration, workflow steps    │
 ├─────────────────────────────────────────────────────────┤
 │                     Domain Layer                        │
 │  - Relational models, core contracts, interfaces      │
 ├─────────────────────────────────────────────────────────┤
 │                  Infrastructure Layer                   │
 │  - FAISS index persistence, SQLAlchemy ORM repos, LLMs  │
 └─────────────────────────────────────────────────────────┘
```

1. **Presentation Layer (`api/`)**:
   - `dependencies/`: Declares dependency injection hooks (injecting database pools, security layers, or search orchestrators cleanly).
   - `middleware/`: Houses request/response filters (CORS wrappers, execution request timing, correlation tracking).
   - `routes/`: Standard REST routers grouped strictly by entity boundary (`auth_router.py`, `document_router.py`, `search_router.py`).
   - `websocket/`: Manages real-time async communication protocols and configurations.
2. **Application Layer (`application/`)**:
   - `constants/`: Global business constants and processing limits.
   - `enums/`: Standard Python Enumeration mappings utilized across use-cases.
   - `schemas/`: Houses request and response Pydantic schemas enforcing data validation boundaries.
   - `services/`: Encapsulates use-case business orchestrators (coordinates multiple models or external actions cleanly).
3. **Core Layer (`core/`)**:
   - `config/`: Dyn-loaded settings mapping environment coordinates securely via Pydantic `BaseSettings`.
   - `exceptions/`: Centralized HTTP and Validation error handlers ensuring consistent REST responses.
   - `logger/`: Timing trackers and structured rotating JSON logs writing daily backups.
   - `security/`: JWT token managers and pass hashing frameworks.
4. **Domain Layer (`domain/`)**:
   - `models/`: Pure SQLAlchemy database ORM models defining database tables cleanly.
   - `interfaces/`: Declarative storage contract protocols (e.g. Repository Interfaces) completely decoupled from database libraries.
5. **Infrastructure Layer (`infrastructure/`)**:
   - `database/`: Database pool contexts, ORM Session builders, and persistent vector drivers (FAISS flat indexes / Qdrant cloud).
   - `repositories/`: Concrete storage query modules implementing the abstract Domain interfaces.
   - `external/`: Gateway clients parsing tokens from external model APIs (Groq, OpenRouter, LM Studio, Ollama).
6. **Shared Layer (`shared/`)**:
   - `helpers/`: Decoupled helper utilities shared across Onion layers.
7. **Storage Module (`storage/`)**:
   - `logs/`: Reserved filesystem directory storing execution rotation logs and runtime errors.
8. **Tests Suite (`tests/`)**:
   - Houses Pytest unit and integration test blocks validating API contracts.

---

### 3.3 Frontend Folder Scaffolding Roles
The frontend employs a feature-driven, decoupled layout where every directory holds a dedicated visual or state role:

1. **`api/`**: Houses central Axios network clients and global TanStack React Query cache definitions.
2. **`assets/`**: Local media elements (glowing icons, logos, vector graphics).
3. **`components/`**: Standalone visual primitives (buttons, glowing boxes, modal inputs) decoupled from feature domains.
4. **`config/`**: Setup variables including i18n configurations and runtime Zod-validated environment configurations (`env.ts`).
5. **`constants/`**: Immutable system constants, labels, and API paths.
6. **`contexts/`**: Global shared context states (e.g. Theme, Authentication) using native React state providers.
7. **`enums/`**: Client-side TypeScript enum definitions.
8. **`features/`**: Functional feature-driven modules (e.g. upload, search, auth). Each folder contains its own local components, state hooks, and Zustand stores to prevent feature bleed.
9. **`hooks/`**: Custom hooks used across multiple features (e.g., `useDebounce`, `useLocalStorage`).
10. **`i18n/`**: System translation catalogs and setups.
11. **`layouts/`**: Master visual containers (like `DashboardLayout` or `AuthLayout`) that organize screen slot structures.
12. **`lib/`**: Custom setup bindings for third-party libraries (e.g. Tailwind styles merging).
13. **`pages/`**: Major view elements representing navigable web screens.
14. **`public/`** (located under `frontend/`): Houses public files (like `vite.svg` or static images) served directly by Vite's asset server without preprocessing.
15. **`routes/`**: React Router client routing directories, including protected auth guards.
16. **`schemas/`**: General input validation structures designed with Zod.
17. **`services/`**: Functional service adapters executing network queries.
18. **`stores/`**: Global state stores implemented using Zustand.
19. **`styles/`**: Global custom stylesheets, utility tokens, and Tailwind v4 configurations.
20. **`tests/`**: Vitest unit and integration test suites validating components and schemas.
21. **`types/`**: Custom TypeScript structural type contracts.
22. **`utils/`**: Text parsers, date formatters, and mathematical calculators.

---

## 4. Ingestion & Retrieval Pipelines

### Ingestion Flow (Document indexing)

1. **Upload**: The user uploads a document through `POST /api/upload` (PDF, DOCX, or TXT).
2. **Parsing**: The extraction service selects PyMuPDF for PDFs, python-docx for DOCX, and plain-text encoders for TXT to extract raw texts.
3. **Chunking**: The parser segments text into recursive blocks of `500` characters, featuring a sliding overlap of `100` characters. This overlap prevents sentence fragmentation.
4. **Embeddings**: Blocks are converted into high-dimensional vectors via the selected embedding provider (configurable to use local sentence-transformers, Groq, OpenRouter, or LM Studio endpoints).
5. **Relational Storage**: Core chunk data and metadata are written to PostgreSQL.
6. **Vector Storage**: Vectors and metadata are upserted into the active vector store (FAISS or Qdrant).
7. **Index Persistence**: If using FAISS, the updated FAISS index is flushed to the disk.

### Retrieval Flow (Semantic search)

1. **Translate Query**: The user types a query, sending it to `POST /api/search`.
2. **Vector Translation**: The query is converted into a vector using the identical embedding provider.
3. **Vector Lookup**: The active vector store performs a similarity search, returning the top `K` matching chunk indexes (default $K=4$).
4. **Fetch database context**: Corresponding textual parts, filenames, and page coordinates are pulled from PostgreSQL.
5. **RAG Prompt Building**: Chunks are assembled into a context window, bounded by a prompt template.
6. **Token SSE Streaming**: The synthesized prompt is passed to the LLM (Groq, OpenRouter, LM Studio, or Ollama). Generated answers are streamed to the React UI in real-time using Server-Sent Events (SSE).
