# 🚀 Quick Start Guide — AI Semantic Search Engine

## 📌 Getting Started

This guide provides a rapid developer bootstrap mapping dependencies, dynamically pluggable configurations, and common workspace tasks.

---

## 🏗️ 1. Quick Ingestion Stack Launch

### A. Backend FastAPI Setup
1. Move into the backend folder:
```bash
cd backend
```
2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows (Git Bash/PowerShell)
source .venv/Scripts/activate
# On macOS/Linux
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up environment variables. Copy `.env.example` into `.env` and verify key settings:
```env
VECTOR_DB_TYPE=faiss  # Options: faiss | qdrant
LLM_PROVIDER=lm-studio  # Options: groq | openrouter | lm-studio | ollama
EMBEDDING_PROVIDER=local  # Options: local | openai | groq | openrouter
```
5. Run the dev server:
```bash
python main.py
```
*The API gateway runs at `http://localhost:8000` with Swagger docs available at `/docs`.*

### B. Frontend React Setup
1. Move into the frontend folder:
```bash
cd frontend
```
2. Install npm modules:
```bash
npm install
```
3. Set up environment variables. Copy `.env.example` into `.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```
4. Start the Vite server:
```bash
npm run dev
```
*The dev layout will open at `http://localhost:5173`.*

---

## 🔑 2. Dynamic Provider Swapping (.env)

Our application is built using concentric onion design boundaries. This allows you to hot-swap infrastructure components cleanly:

### Vector Databases
* **FAISS**: Works locally out of the box using flat file vectors index. No cloud installation needed. Set `VECTOR_DB_TYPE=faiss`.
* **Qdrant**: High-performance semantic vector database. Perfect for cloud deployments. Set `VECTOR_DB_TYPE=qdrant` and declare `QDRANT_URL` and `QDRANT_API_KEY`.

### LLM Providers
Set `LLM_PROVIDER` to one of the following:
* **`lm-studio`**: Run a local GGUF model via LM Studio on `http://localhost:1234/v1`.
* **`ollama`**: Run a local offline LLM via Ollama on `http://localhost:11434`.
* **`groq`**: Fast cloud-hosted inference. Needs a valid `GROQ_API_KEY`.
* **`openrouter`**: Aggregated gateways. Needs a valid `OPENROUTER_API_KEY`.

---

## 📁 3. Core Structural Files & Mappings

```text
src/
├── api/                # Network adapters & Axios query endpoints
├── components/         # Premium global primitives (glowing button, input boxes)
├── config/             # Environment schemas & Zod validations (env.ts)
├── features/           # Modular features (upload, search, auth) with local hooks/stores
├── layouts/            # Master layout page templates (DashboardLayout)
├── routes/             # Client-side router maps & guarded auth filters
├── stores/             # Global Zustands state managers (authStore, searchStore)
└── styles/             # Tailwind utility configs & layout styling variables
```

| Crucial File | Architectural Purpose |
| :--- | :--- |
| `frontend/src/main.tsx` | UI DOM initialization point loaded with React 19 router wrappers |
| `frontend/src/env.ts` | Strict Zod validation parsing `import.meta.env` keys on startup |
| `backend/src/main.py` | Asynchronous FastAPI gateway, loading dependency injection pools |
| `backend/src/core/config/config.py` | Syncs environment settings leveraging Pydantic BaseSettings |

---

## 🎯 4. Common Developer Tasks

### Add a New Screen/Page
1. Create a page file inside `frontend/src/pages/YourNewPage.tsx`.
2. Map the path route inside `frontend/src/routes/index.tsx`.
3. Link the path cleanly in the side dashboard layout at `frontend/src/layouts/DashboardLayout.tsx`.

### Create a Custom API Service
1. Create a service adapter file inside `frontend/src/services/yourService.ts`.
2. Configure Axios calls using the default client:
```typescript
import { apiClient } from "@/api/client";

export const yourService = {
  fetchData: async (id: string) => {
    const response = await apiClient.get(`/your-endpoint/${id}`);
    return response.data;
  }
};
```

---

## 🔧 5. Local Troubleshooting Guidelines

### Vitest Validation Fails
* **Symptom**: Environment schema throws Zod parsing errors in Vitest runner.
* **Resolution**: The `import.meta.env` variable may not be present inside Vitest mock runtime. Check `frontend/src/tests/env.test.ts` to see how envSchema parsing is safe-parsed. Ensure Vitest does not load the active environment schema directly on test boot.

### SQLite/Postgres Async Connection Fails
* **Symptom**: Backend boot logs throw database driver errors.
* **Resolution**: Check the active connection URL `DATABASE_URL` in `backend/.env`. Ensure you use correct async prefix strings (e.g. `sqlite+aiosqlite:///` or `postgresql+asyncpg://`).

### FAISS Index Lock (Windows OS)
* **Symptom**: `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
* **Resolution**: Occurs when multiple asynchronous tasks attempt to write updates into the identical flat vector `.index` files simultaneously. Set proper read/write threading guards, or transition to dynamically hosting `qdrant` as the vector store.
