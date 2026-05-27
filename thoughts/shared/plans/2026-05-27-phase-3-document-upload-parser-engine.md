# Phase 3: Document Upload & Parser Engine Implementation Plan

**Date:** May 27, 2026  
**Status:** Ready for Implementation  
**Priority:** High  
**Estimated Effort:** 12-16 hours  

---

## 1. Executive Summary

This plan outlines the design and implementation of the document ingestion pipeline for the **AI Semantic Search Engine**. The parser engine is responsible for accepting user-uploaded documents, extracting their raw text coordinates, splitting the extracted content into semantic overlapping segments, and storing these chunks within our PostgreSQL database. 

**Key Objectives:**
- Resilient file ingestion of `PDF`, `DOCX`, and `TXT` files via a secure multi-part endpoint.
- High-fidelity text extraction: extracting characters, page numbers, and exact page coordinates (using `PyMuPDF` for PDF).
- Bounded semantic chunking: overlapping text segments (500 characters with 100 character sliding overlap) to maintain contextual coherence.
- Responsive, drag-and-drop React upload interface displaying real-time parser status.

---

## 2. Pre-Implementation Verification & Setup

### Required Libraries
- **PDF Extraction:** `PyMuPDF` (`fitz`) — lightweight and fast.
- **DOCX Extraction:** `python-docx`.
- **Text Extraction:** Python base libraries with encoding auto-detection (e.g., utf-8, latin-1).

### Database Model Prerequisite
Ensure that the `documents` and `chunks` relational tables are mapped accurately inside SQLAlchemy ORM definitions in the Domain layer before building ingestion workflows.

---

## 3. Onion Layer Architecture Mapping

The document pipeline aligns with our concentric Onion boundaries:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│  - backend/src/api/routes/document_router.py          │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│  - backend/src/application/services/parser_service.py │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌────────────────────────────────────────────────────────┐
│                     Domain Layer                       │
│  - backend/src/domain/models/document.py              │
│  - backend/src/domain/models/chunk.py                 │
└────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Implementation Tasks

### Task 1: Domain Mapping (Document & Chunk)
**Estimated Time:** 2 hours  
**Risk Level:** Low  
**Files:** 
- `backend/src/domain/models/document.py`
- `backend/src/domain/models/chunk.py`

**Steps:**
1. Define the `Document` SQLAlchemy model: `id` (UUID), `user_id` (UUID), `file_name`, `file_path`, `file_size`, `file_type`, `status` (`uploaded`, `processing`, `indexed`, `failed`), and `created_at`.
2. Define the `Chunk` SQLAlchemy model: `id` (UUID), `document_id` (UUID, foreign key), `content` (text), `page_number` (integer), `chunk_index` (integer), `metadata` (JSONB), and `created_at`.
3. Create database indices on `chunks.document_id` and JSONB `metadata` to speed up future semantic lookups.

**Success Criteria:**
- Relational mapping compiles cleanly.
- Cascade deletions are configured correctly (deleting a document drops all corresponding chunks).

---

### Task 2: Core Text Extraction Adapters
**Estimated Time:** 3.5 hours  
**Risk Level:** Medium  
**Files:** `backend/src/application/services/parser_service.py`

**Steps:**
1. Implement the extraction interface `BaseExtractor` exposing an async `extract` method.
2. Build `PDFExtractor` utilizing `PyMuPDF` (`fitz`):
   - Open PDF file stream.
   - Iterate through pages, capturing `page_number`, text content, and metadata.
   - Extract page dimensions to preserve visual reference points.
3. Build `DocxExtractor` using `python-docx` to loop through paragraphs and tables.
4. Build `TextExtractor` handling fallback decoding for `.txt` assets.

**Success Criteria:**
- Extractors handle multi-page documents without high memory bloat.
- Special symbols and line breaks are decoded cleanly.

---

### Task 3: Bounded Overlapping Chunking Engine
**Estimated Time:** 2.5 hours  
**Risk Level:** Low  
**Files:** `backend/src/application/services/chunker.py`

**Steps:**
1. Implement a semantic sliding text splitter:
   - Input: Raw extracted text per page.
   - Target Chunk Size: `500` characters.
   - Sliding Overlap: `100` characters.
2. Ensure chunk boundaries respect sentence boundaries where possible to avoid context clipping.
3. For each chunk, assemble a metadata payload: `{ "page_number": X, "chunk_index": Y, "file_name": Z }`.

**Success Criteria:**
- Splitter generates chunks exactly bounded by specified characters.
- Word and sentence context remains intact across overlap bounds.

---

### Task 4: Ingestion Controller & Route Setup
**Estimated Time:** 3 hours  
**Risk Level:** Medium  
**Files:** `backend/src/api/routes/document_router.py`

**Steps:**
1. Implement `POST /documents/upload` accepting multi-part form data uploads.
2. Persist the raw file to local storage or an isolated storage folder safely.
3. Trigger the parser service asynchronously (using FastAPI `BackgroundTasks` to avoid holding up the HTTP response).
4. Implement `GET /documents` to fetch upload history and parsing status.

**Success Criteria:**
- Files upload successfully and trigger background extraction.
- Parsing failures update the document status to `failed` and log execution traces cleanly.

---

### Task 5: Drag-and-Drop Ingestion Interface
**Estimated Time:** 3.5 hours  
**Risk Level:** Low  
**Files:** 
- `frontend/src/features/upload/components/UploadDropzone.tsx`
- `frontend/src/features/upload/components/DocumentList.tsx`

**Steps:**
1. Design a premium dropzone featuring subtle neon borders, glassmorphic backgrounds, and drag-over animations.
2. Implement file size validation (e.g. limit to 10MB) and extension checks.
3. Use a custom hook to query the document list, displaying upload progress bars and parsing states (`processing` -> `indexed`).

**Success Criteria:**
- Component supports seamless drag-and-drop upload.
- List updates state reactively using TanStack query polling.

---

## 5. Testing & Verification Strategy

### Manual Verification Checklist
- [ ] Drop a multi-page PDF into the UI; verify file status transitions cleanly.
- [ ] Verify database contains the raw document row and corresponding chunk rows.
- [ ] Ensure that chunks include accurate page numbers and sequence indexes.
- [ ] Test uploading invalid file types (e.g. `.exe`, `.png`); ensure dropzone displays elegant error messages.

### Automated Tests
- Test PDF extractor with mock multi-page bytes.
- Test text chunker utility with custom character thresholds (assert overlap math holds).
- Mock `BackgroundTasks` to test the API controllers synchronously.

---

## 6. Risk Assessment

| Risk Category | Details | Mitigation Strategy |
| :--- | :--- | :--- |
| **High: Memory Bloat** | Large documents (e.g. 100+ pages) parsed in-memory exhaust RAM, crashing backend containers. | Use streaming generators to process documents page-by-page. Garbage-collect document handles immediately. |
| **Medium: Character overlap drift** | Text chunks become misaligned or overlapping logic errors drop characters. | Write strict unit tests assert that character index sums equal raw document length. |
