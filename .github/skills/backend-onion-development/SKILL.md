---
name: backend-onion-development
description: Enforces concentric Onion boundaries, strict typing, async execution, and SQLAlchemy 2.0 ORM conventions.
---

# Skill: Backend Onion Development (FastAPI + SQLAlchemy)

This skill provides step-by-step instructions for implementing, refactoring, or extending backend logic within the concentric 4-layer Onion Architecture boundary.

---

## 🏛️ Onion Layer Architecture Mapping

When coding backend features, allocate your files strictly as follows:

1. **api/routes/**: Exposes controllers, dependencies, and FastAPI endpoints.
2. **application/services/**: Coordinates business workflows and encapsulates use-case triggers.
3. **domain/models/**: Relational database models (SQLAlchemy ORM definitions).
4. **domain/interfaces/**: Core storage contracts (interfaces defining Repository methods).
5. **infrastructure/repositories/**: Concrete storage classes implementing Domain Interfaces.

Never import from an outer layer to an inner layer (e.g. do not import models or repositories inside interfaces).

---

## 🔒 Relational DB Conventions (SQLAlchemy 2.0)

- Use only asynchronous query syntax (`await session.execute`).
- Leverage Eager Loading options (`joinedload`, `selectinload`) to prevent high-latency N+1 transaction loops.
- Handle Relational Sessions safely with transaction try-except boundaries:
  ```python
  async with session.begin():
      # Relational writes here...
  ```
- Keep Relational Models decoupled from Presentation outputs by mapping responses to Pydantic v2 schemas.
