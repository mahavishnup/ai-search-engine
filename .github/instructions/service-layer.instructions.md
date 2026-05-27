---
appliesTo: ["**/application/services/**"]
---

# Service Layer Instructions

## Service Class Patterns

Service classes orchestrate business logic and coordinate between repositories and external services. They should be stateless and depend only on repositories and infrastructure services.

### Basic Service Structure

**Reference**: `examples/services/user_service.py.example` for complete service implementation patterns.

Key patterns:
- Use dependency injection with `Annotated[RepositoryClass, Depends()]`
- All methods must be async
- Implement business logic and orchestration
- Handle errors with appropriate HTTP exceptions
- Convert between repository data and Pydantic models

### Error Handling Patterns

**Reference**: `examples/services/user_service.py.example` contains comprehensive error handling examples.

Always handle errors appropriately and return meaningful HTTP exceptions:
- Validate input parameters early
- Handle specific business logic errors with appropriate HTTP status codes
- Re-raise HTTPExceptions, catch and convert other exceptions
- Use meaningful error messages

### Business Logic Examples

**Reference**: `examples/services/user_service.py.example` for complete business logic implementations.

#### Key Business Logic Patterns
- **Data Validation**: Validate business rules before repository calls
- **Data Processing**: Transform and normalize input data
- **Uniqueness Checks**: Verify constraints like unique emails
- **Status Transitions**: Implement complex state management logic

### Working with Multiple Repositories

**Reference**: `examples/shared/patterns.py.example` for dependency injection patterns with multiple services.

Services can depend on multiple repositories to coordinate complex operations:
- Inject multiple repository dependencies
- Handle operations that span multiple data sources
- Manage transaction boundaries when needed
- Implement compensation logic for failures

### Pagination Service Pattern

**Reference**: `examples/services/user_service.py.example` contains complete pagination implementation.

Key pagination patterns:
- Validate pagination parameters (page, per_page limits)
- Calculate offset from page numbers
- Return structured response with metadata
- Handle edge cases (empty results, invalid pages)

### Infrastructure Integration

**Reference**: `examples/shared/patterns.py.example` for infrastructure dependency patterns.

When working with external services (storage, auth, etc.):
- Inject infrastructure services as dependencies
- Handle external service failures gracefully
- Implement proper error handling and retries
- Keep infrastructure concerns separate from business logic

## Service Layer Best Practices

1. **Keep services stateless** - No instance variables except dependencies
2. **Handle all business logic** - Don't leak business rules to controllers or repositories
3. **Use proper error handling** - Convert internal errors to appropriate HTTP exceptions
4. **Validate input early** - Check business rules before calling repositories
5. **Use transactions when needed** - Coordinate multiple repository operations
6. **Document complex operations** - Include docstrings explaining business logic
7. **Keep dependencies minimal** - Only inject what you actually need
8. **Make async operations explicit** - All service methods should be async
9. **Return appropriate models** - Always return response models, not raw data
10. **Handle edge cases** - Consider null values, empty results, and error scenarios