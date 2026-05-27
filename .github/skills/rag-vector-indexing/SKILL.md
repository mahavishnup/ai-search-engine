---
name: rag-vector-indexing
description: Enforces FAISS boundary safety, sliding overlap text segmentations, and Server-Sent Events (SSE) streaming protocols.
---

# Skill: RAG & Vector Indexing Specialist

This skill covers rules for document text splitting, local vector indexing, and streaming answers.

---

## ⚙️ Ingestion & Chunking Bounds
- **Overlapping Segmentation**: Segment document parsed texts recursive-wise:
  - **Chunk Size**: `500` characters.
  - **Sliding Overlap**: `100` characters.
- **Metadata Captures**: Retain page coordinate grids and exact page integers during PyMuPDF parsing to support source citations.

---

## 📊 Local FAISS Index Protection
- Ensure vector allocations map correctly with Postgres chunk primary keys.
- Write indices safely on disk, reloading them dynamically on application startup.
- Yield tokens incrementally over `text/event-stream` SSE configurations, terminating with a clear `[DONE]` indicator block.
