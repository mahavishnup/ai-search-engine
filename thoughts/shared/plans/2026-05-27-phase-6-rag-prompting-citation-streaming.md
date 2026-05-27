# Phase 6: RAG LLM & Citation Service (Streaming) Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 10-14 hours  

---

## 1. Executive Summary

This plan outlines the architecture and execution of the pluggable Retrieval-Augmented Generation (RAG) streaming interface for the **AI Semantic Search Engine**. Operating under **Pydantic Validation** and standard **Onion concentric boundaries**, this phase coordinates prompt builders, streaming LLM services, and citation generators.

We support a **multi-provider LLM gateway** selectable via `.env` variables, allowing developers and users to toggle between:
- **Groq (`LLM_PROVIDER=groq`)**: Lightning-fast cloud LPUs.
- **OpenRouter (`LLM_PROVIDER=openrouter`)**: Unified cloud model proxy gateway.
- **LM Studio (`LLM_PROVIDER=lm-studio`)**: Local, offline, zero-cost OpenAI-compatible server at `http://localhost:1234/v1`.
- **Ollama (`LLM_PROVIDER=ollama`)**: Local model execution server on port `11434`.

---

## 2. Pre-Implementation Verification & Setup

### Requirements
- Active Semantic Search Service (Phase 5).
- Local offline model servers (LM Studio / Ollama) active on their respective ports if local provider is chosen.
- Access credentials and API keys for cloud gateways if cloud provider is chosen.

### Grounding System Prompt
```text
You are a Semantic Search Assistant. Answer the USER's Query using ONLY the following verified context.
If the context does not contain the answer, say "I cannot find this information in your documents." Do not invent facts.

Context:
---
[Source: {filename}, Page: {page}]
{content}
---

Query: {user_query}
```

---

## 3. Onion Layer Architecture Mapping

All components map cleanly inside concentric Onion layers:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/chat_router.py              │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/services/prompt_builder.py │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│  - backend/src/infrastructure/external/llm_client.py   │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Context Prompt Synthesis Module
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** `backend/src/application/services/prompt_builder.py`

**Steps:**
1. Code `PromptBuilder` coordinating retrieved chunk aggregations.
2. Construct system guidelines enforcing strict facts grounding:
   - Prevent hallucination or external knowledge leakage.
   - Enforce explicit citation markers (e.g., `[^source_idx]`) inside generated sentences.
3. Handle token size caps to avoid exceeding model context limits.

**Success Criteria:**
- Prompts assemble text chunks and instructions cleanly.
- Grounding limits prevent the model from generating answers outside the context.

---

### Task 2: Pluggable Multi-Provider Async LLM Client
**Estimated Time:** 4 hours  
**Risk Level:** Medium  
**Files:** `backend/src/infrastructure/external/llm_client.py`

**Steps:**
1. Code the abstract streaming connector interface `ILLMProvider`.
2. Implement `LLMStreamProvider` coordinating config-driven model selection from `.env`:
   - **groq** / **openrouter**: Initialize cloud-based `httpx` HTTP clients routing standard API payload formats.
   - **lm-studio**: Route standard OpenAI-compatible requests targeting local address: `http://localhost:1234/v1/chat/completions`.
   - **ollama**: Direct JSON payloads targeting Ollama's local address: `http://localhost:11434/api/chat`.
3. Implement dynamic streaming generators yielding token characters sequentially as they load.

**Success Criteria:**
- Streaming client resolves API responses incrementally.
- Deployed system toggles LLM providers dynamically via `.env` updates with zero code modifications.

---

### Task 3: Streaming Controller (SSE Router)
**Estimated Time:** 4 hours  
**Risk Level:** High  
**Files:** `backend/src/api/routes/chat_router.py`

**Steps:**
1. Code API route `POST /api/chat/stream` returning a FastAPI `StreamingResponse`.
2. Core Generator logic:
   - Retrieve top-K relevant chunks for the user's query using the active vector store (FAISS/Qdrant).
   - Assemble context prompt using `PromptBuilder`.
   - Format source document citations into an initial `metadata` SSE packet: `data: {"type": "metadata", "sources": [...]}`.
   - Stream the LLM response tokens sequentially: `data: {"type": "token", "content": "..."}`.
   - Yield final termination indicator: `data: [DONE]`.
3. Save completed query and final answer to `search_history` in database.

**Success Criteria:**
- Stream sends valid `text/event-stream` chunks.
- Relational history records write correctly upon stream termination.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Set `LLM_PROVIDER=lm-studio` in `.env`, boot your local LM Studio model server, and trigger a query; verify logs capture local OpenAI-compatible routing.
- [ ] Set `LLM_PROVIDER=groq` in `.env` and trigger a search; verify lightning-fast cloud streaming responses.
- [ ] Ask a question unrelated to uploaded documents; ensure the model correctly refuses to answer, maintaining factual grounding.

### Automated Tests
- Test streaming endpoint using `httpx.AsyncClient` parsing events.
- Assert database history entries match the final text output of the stream.
- Test client connection aborts (ensure backend closes LLM connections and releases resources immediately).

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Hanging client connections** | Users aborting streams leaves open backend sockets, rapidly exhausting server worker threads. | Detect client disconnection events cleanly (`await request.is_disconnected()`) and break generator loops instantly. |
| **Medium: Local Hardware Bottlenecks** | Local servers (LM Studio, Ollama) timing out on low-spec hardware during heavy concurrent loads. | Implement request timeouts and connection fallbacks gracefully. |
