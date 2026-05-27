# AI-Powered Semantic Search Engine (RAG)

An enterprise-grade, beginner-friendly AI Semantic Search Engine built using a React + Vite + TypeScript frontend, a FastAPI microservices-ready backend (Onion Architecture), local FAISS vector store indexing, PostgreSQL relational DB, and integrated LLM RAG pipelines.

---

## 1. Key Features

- **Semantic Vector Match**: High-dimensional cosine similarity matching powered by FAISS vector indexing (or Qdrant cloud/local vector database).
- **RAG Generation**: Contextually grounded answers with streaming responses (SSE) using Groq, OpenRouter, NVIDIA, or local offline servers like LM Studio and Ollama.
- **Granular Citations**: Full source tracking displaying source filenames and exact document page numbers.
- **Onion Architecture**: Decoupled, 4-layer backend layout inside FastAPI ensuring clean codebase scalability.
- **Feature-Driven UI**: Beautiful React 19+ application utilizing Tailwind, Zustand stores, and TanStack React Query.

---

## 2. Workspace Layout

The repository utilizes a modular, feature-driven structure:

```text
ai-search-engine/
 ├── .claude/               # Anthropic Claude Code configurations
 ├── .gemini/               # Google Gemini / Antigravity configurations
 ├── .github/               # Unified GitHub CI, workflows, modular guidelines, prompts & skills
 ├── backend/               # FastAPI Backend Gateway Service (Onion Architecture)
 ├── frontend/              # React + Vite feature-driven frontend web app
 ├── .agent.md              # AI agent master rules configuration
 ├── CLAUDE.md              # Claude CLI workspace instructions
 ├── GEMINI.md              # Gemini / Antigravity workspace instructions
 ├── copilot.md             # GitHub Copilot prompts & instructions
 ├── PROJECT_PLAN.md        # Master 14-Phase Implementation Document
 ├── ARCHITECTURE.md        # Detailed Architecture & Pipeline Guide
 └── README.md              # Developer Quickstart & Installation Setup
```

---

## 3. Prerequisite Stack

Ensure you have the following installed locally:
- **Node.js**: v22.x or newer
- **Python**: v3.12.x or newer
- **PostgreSQL**: v15.x or newer
- **Redis** (Optional): For caching setup
- **Docker & Compose**: For microservices orchestration
- **LM Studio / Ollama** (Optional): For local offline LLM testing

---

## 4. Setup & Running Locally

### A. Backend Service Setup
1. Move to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows (Git Bash / PowerShell)
   source .venv/Scripts/activate
   # On macOS / Linux
   source .venv/bin/activate
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `backend/.env` (see `backend/.env.example` for all options):
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./data/app.db
   VECTOR_DB_TYPE=faiss  # Options: faiss | qdrant
   LLM_PROVIDER=lm-studio  # Options: groq | openrouter | lm-studio | ollama
   EMBEDDING_PROVIDER=local  # Options: local | openai | groq | openrouter
   ```
5. Run the FastAPI dev server:
   ```bash
   python main.py
   # Or using uvicorn
   uvicorn src.main:app --reload
   ```

### B. Frontend Service Setup
1. Move to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables in `frontend/.env`:
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   ```
4. Run frontend tests:
   ```bash
   npm run test
   ```
5. Start the Vite local server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` on your browser to view the application UI.

---

## 5. Dockerized Orchestration

To boot the entire stack (React FE, FastAPI BE, PostgreSQL DB, Redis) with a single command:
1. Ensure Docker is running.
2. Spin up containers from the root directory:
   ```bash
   docker-compose up --build
   ```
3. Stop the containers:
   ```bash
   docker-compose down -v
   ```
