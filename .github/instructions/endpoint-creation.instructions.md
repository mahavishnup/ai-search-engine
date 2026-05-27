---
appliesTo: ["**/api/**", "**/application/services/**", "**/infrastructure/repositories/**"]
---

# Endpoint Creation Instructions

## Complete Endpoint Creation Workflow

When creating a new endpoint, follow this exact sequence to maintain architectural consistency:

### Step 1: Define Pydantic Models

Create request/response models in `src/application/models/`.

**Reference implementation**: `examples/models/user_models.py.example`

Key patterns to follow:

- Use `BaseRequest` for input models (prevents extra fields)
- Use `BaseResponse` for output models (allows ORM attribute access)
- Include proper type annotations with Optional types
- Add descriptive docstrings for API documentation
- Use descriptive model names ending in Request/Response

### Step 2: Create Repository Class

Create data access layer in `src/infrastructure/repositories/{resource}_repository.py`.

**Reference implementation**: `examples/repositories/user_repository.py.example`

Key patterns to follow:

- Use dependency injection with `Annotated[AsyncSession, Depends(get_session)]`
- All methods must be async
- Use SQLAlchemy `text()` for raw SQL queries
- Proper session management and error handling
- Return dictionaries that can be converted to Pydantic models
- Support both PostgreSQL and MSSQL based on infrastructure selection

### Step 3: Create Service Class

Create business logic in `src/application/services/{resource}_service.py`.

**Reference implementation**: `examples/services/user_service.py.example`

Key patterns to follow:

- Use dependency injection with `Annotated[RepositoryClass, Depends()]`
- All methods must be async
- Implement business logic and orchestration
- Handle errors with appropriate HTTP exceptions
- Convert between repository data and Pydantic models
- Coordinate multiple repository calls when needed

### Step 4: Create Router

Create HTTP endpoints in `src/api/{resource}_router.py`.

**Reference implementation**: `examples/api/user_router.py.example`

Key patterns to follow:

- Use dependency injection with `Annotated[ServiceClass, Depends()]`
- All endpoint functions should be async
- Include proper HTTP status codes
- Add comprehensive docstrings for Swagger documentation
- Use appropriate response models
- Handle query parameters for filtering and pagination
- Follow RESTful conventions

### Step 5: Register Router

Update `src/api/__init__.py` to include your new router.

**Pattern**: Import your router and add it to the v1_router with `include_router()`.
See the end of `examples/api/user_router.py.example` for the exact registration pattern.

## Common Endpoint Patterns

### CRUD Operations Template

**Reference**: `examples/api/user_router.py.example` contains complete CRUD examples.

Standard HTTP methods and status codes:

- **CREATE**: `POST /` with `status_code=201`
- **READ (single)**: `GET /{resource_id}`
- **READ (list)**: `GET /` with pagination parameters
- **UPDATE**: `PUT /{resource_id}`
- **DELETE**: `DELETE /{resource_id}` with `status_code=204`

### Pagination and Query Parameters

**Reference**: `examples/shared/patterns.py.example` contains pagination and filtering patterns.

Use `Query()` parameters for pagination, filtering, and search functionality.

## Important Rules

1. **Always create all 4 layers** even for simple endpoints
2. **Use async/await** throughout the entire stack
3. **Include proper error handling** with meaningful HTTP status codes
4. **Add docstrings** to all endpoint functions for Swagger documentation
5. **Follow naming conventions**: `{resource}_router.py`, `{resource}_service.py`, etc.
6. **Register new routers** in the appropriate `__init__.py` file
7. **Use type annotations** for all parameters and return values
8. **Import models** from the application layer, not directly from repositories

## Reference Files Summary

- **`examples/models/user_models.py.example`** - Pydantic model patterns
- **`examples/repositories/user_repository.py.example`** - Repository layer patterns
- **`examples/services/user_service.py.example`** - Service layer patterns
- **`examples/api/user_router.py.example`** - Router and endpoint patterns
- **`examples/shared/patterns.py.example`** - Common imports, conventions, and utilities
