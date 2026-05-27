# Prompt Template: Create New Backend Feature

Use this prompt to instruct any AI developer assistant to build a new feature inside the FastAPI backend.

---

## Instructions to Agent:

"Please design and build a new feature inside the 'backend/src/' repository layer. You must strictly follow our **4-Layer Onion Architecture** standards defined in 'ARCHITECTURE.md' and '.agent.md'.

### Step-by-Step Execution Checklist:

1. **Domain Layer (Models & Contracts)**:
   - If a database schema modification is required, write the SQLAlchemy 2.0 ORM model in 'domain/models/'.
   - Declare the abstract repository interface (contract) in 'domain/interfaces/'.
2. **Application Layer (Use Cases & Schemas)**:
   - Create Pydantic v2 schemas (`BaseRequest`/`BaseResponse` templates) in 'application/schemas/'.
   - Code the business logic / use-case orchestrator class inside 'application/services/'. Ensure it depends strictly on repository interfaces, not concrete implementations.
3. **Infrastructure Layer (Concrete Persistence)**:
   - Implement the repository interface in 'infrastructure/repositories/' utilizing async SQLAlchemy `SessionLocal`.
4. **Presentation Layer (API Controller Routes)**:
   - Bind the use case inside a new router in 'api/routes/', injecting database sessions and service instances via FastAPI `Depends()`.

### Code Style Specifications:

- Declare strict, complete Python type annotations (e.g. `Annotated[T, Depends(...)]`).
- Wrap relational queries in secure transaction blocks. Roll back session state if any error occurs.
- Write direct, meaningful logs showing execution duration and boundary entries."
