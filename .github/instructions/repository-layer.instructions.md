---
appliesTo: ["**/infrastructure/repositories/**"]
---

# Repository Layer Instructions

## Repository Pattern Implementation

Repositories provide data access abstraction and should be the only layer that directly interacts with databases or external data sources. They handle database sessions, queries, and data mapping.

### Basic Repository Structure

**Reference**: `examples/repositories/user_repository.py.example` for complete repository implementation patterns.

Key patterns:

- Use dependency injection with `Annotated[AsyncSession, Depends(get_session)]`
- All methods must be async
- Use SQLAlchemy `text()` for raw SQL queries
- Proper session management and error handling
- Return dictionaries that can be converted to Pydantic models
- Support both PostgreSQL and MSSQL based on infrastructure selection

### CRUD Operations Patterns

**Reference**: `examples/repositories/user_repository.py.example` contains complete CRUD implementations.

#### Key Operation Patterns

- **Create**: Use `INSERT ... RETURNING` to get generated IDs and timestamps
- **Read**: Support both single record and list operations
- **Update**: Use dynamic updates with validation
- **Delete**: Return success status or row count
- **Error Handling**: Wrap operations in try/catch with session rollback

### Advanced Query Patterns

**Reference**: `examples/repositories/user_repository.py.example` for comprehensive query examples.

#### Pattern Categories

- **Search and Filtering**: Dynamic WHERE clauses with optional parameters
- **Complex Joins**: Multi-table queries with relationships
- **Aggregations**: Statistical queries with GROUP BY and aggregate functions
- **Pagination**: LIMIT/OFFSET patterns with total count queries
- **Bulk Operations**: Efficient multi-record operations

### Database-Specific Patterns

**PostgreSQL**: Use `RETURNING` clauses, `ILIKE` for case-insensitive search, `NOW()` for timestamps
**MSSQL**: Use `OUTPUT` clauses, `GETDATE()` for timestamps, different syntax patterns

### Transaction Management

**Reference**: `examples/repositories/user_repository.py.example` for transaction handling patterns.

Key transaction principles:

- Use try/catch with session rollback on errors
- Coordinate multiple operations within single transactions
- Handle both hard and soft delete patterns
- Implement proper audit trails for complex operations

## Repository Best Practices

1. **Use parameterized queries** - Always use `:parameter` syntax to prevent SQL injection
2. **Handle transactions properly** - Use commit/rollback appropriately
3. **Return consistent data types** - Always return dictionaries or None for single records
4. **Include error handling** - Let exceptions bubble up to service layer
5. **Use appropriate SQL features** - Leverage database-specific features when available
6. **Keep queries readable** - Use proper formatting and comments for complex queries
7. **Optimize for performance** - Use indexes, limit results, and avoid N+1 queries
8. **Make methods async** - All repository methods should be async
9. **Document complex queries** - Include comments explaining business logic in SQL
10. **Use consistent naming** - Follow `verb_noun` pattern (get_user, create_user, etc.)
