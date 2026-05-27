# Phase 7: React Search Interface & Zustand Stores Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 10-12 hours  

---

## 1. Executive Summary

This plan outlines the frontend state architecture and interface components for the **AI Semantic Search Engine**. Designed with standard **TypeScript Interfaces** and feature-driven layouts, this phase connects the backend search and streaming endpoints (Phases 5 & 6) to a premium, real-time user interface. It establishes our state management framework and builds our core interactive RAG query interface.

**Key Deliverables:**
- Zustand global stores (`store/searchStore.ts`, `store/chatStore.ts`) managing UI state, history, and real-time streaming chunks.
- Autogrowing Search Input component with smart keystroke listeners (e.g. Enter to send, Shift+Enter to newline).
- Streaming chat renderer with complete Markdown parsing support.
- Expandable citation components connecting generated sentences to exact source chunks.

---

## 2. Pre-Implementation Verification & Setup

### Requirements
- Complete and verified streaming endpoints on backend.
- Core packages installed: `zustand`, `lucide-react`, `react-markdown`, `remark-gfm`.

---

## 3. Detailed Implementation Tasks

### Task 1: Zustand Global State Stores
**Estimated Time:** 3 hours  
**Risk Level:** Low  
**Files:** 
- `frontend/src/stores/searchStore.ts`
- `frontend/src/stores/chatStore.ts`

**Steps:**
1. Code `searchStore.ts` to manage:
   - Traditional text search query, loading flag, result nodes, and errors.
2. Code `chatStore.ts` to orchestrate streaming chat:
   - Message array containing `{ role: 'user' | 'assistant', content: str, sources: list }`.
   - Streaming state properties (indicates whether stream is active).
   - Async action `sendMessage(query: str)` executing SSE connections (using standard browser `EventSource` or `fetch-event-source` for POST requests).
   - Real-time token appending handler.

**Success Criteria:**
- Zustand store handles streaming content changes reactively.
- Errors are captured and clear loading flags are set cleanly during API operations.

---

### Task 2: Autogrowing Search Input Component
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `frontend/src/features/search/components/SearchInput.tsx`

**Steps:**
1. Build a text-area search bar featuring autogrowing heights (up to a max height of 200px) that adjusts dynamically based on content.
2. Apply premium styling matching the theme: glassmorphism (`bg-background/80 backdrop-blur`), subtle glowing rings on focus, and smooth transitions.
3. Configure keyboard shortcuts:
   - `Enter` triggers submission.
   - `Shift + Enter` inserts a newline character safely.
4. Add clear indicator buttons and loading spinners when query execution is active.

**Success Criteria:**
- Textarea grows and shrinks reactively with zero scroll bar flickers.
- Quick submissions launch query actions seamlessly.

---

### Task 3: Streaming Conversation Renderer
**Estimated Time:** 4 hours  
**Risk Level:** Medium  
**Files:** 
- `frontend/src/features/search/components/ChatWindow.tsx`
- `frontend/src/features/search/components/ChatMessage.tsx`

**Steps:**
1. Build `ChatWindow` listing the conversation history.
2. For assistant messages:
   - Use `react-markdown` and `remark-gfm` to parse formatting, bold highlights, lists, and code blocks cleanly.
   - Parse custom inline citation tags (e.g., `[^1]`) and replace them with interactive clickable superscript numbers.
3. Add a smooth auto-scroll helper that keeps the viewport at the bottom of the page as new tokens stream in, unless the user has manually scrolled up.

**Success Criteria:**
- Stream tokens render without layout shifts.
- Clickable citation indices match the retrieved source array.

---

### Task 4: Rich Citation Drawer / Accordion
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `frontend/src/features/search/components/CitationList.tsx`

**Steps:**
1. Design an interactive expandable accordion list positioned at the footer of each assistant message.
2. Each source card displays:
   - Document name and index.
   - Exact page coordinate details.
   - High-fidelity text snippet of the retrieved chunk.
3. Map inline superscript click triggers to highlight or scroll to the respective source card.

**Success Criteria:**
- Citations display transparent, clean user interaction paths.
- Source snippets expand and collapse smoothly.

---

## 4. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Type a prompt and submit; verify the chat window appends messages and streams text token-by-token.
- [ ] Verify that scrolling up during active generation pauses auto-scrolling to prevent layout locking.
- [ ] Click an inline citation superscript tag; ensure it highlights the correct source card.

### Automated Tests
- Test Zustand `chatStore` logic using mock stream data.
- Verify message parser regex successfully converts different citation string variations.
- Ensure that textareas handle multiple fast return keys without submitting empty strings.

---

## 5. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **Medium: Layout Shifts** | Rapid token streaming updates cause layout jumping, creating poor user experiences. | Define solid, fixed-height shells for message containers and scroll yards. |
| **Low: Stream interruptions** | Network connection drops during stream leaves UI stuck in loading state. | Set up explicit timeout limits and connection drop callbacks that reset state and display error banners. |
