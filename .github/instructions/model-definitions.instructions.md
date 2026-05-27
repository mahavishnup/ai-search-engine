---
appliesTo: ["**/application/schemas/**"]
---

# Model Definitions Instructions

## Pydantic Model Patterns

Pydantic models define data structures for API requests and responses. They provide validation, serialization, and documentation for your FastAPI endpoints.

### Model Organization Structure

```
app/application/schemas/
├── shared/
│   └── schemas.py          # Base classes (BaseRequest, BaseResponse, PaginatedResponse)
├── user_schemas.py        # User-related models
├── product_schemas.py     # Product-related models
└── auth_schemas.py        # Authentication models
```

### Base Model Classes Usage

**Reference**: `examples/schemas/user_models.py.example` for complete model patterns.

Always inherit from the appropriate base class:

- **BaseRequest**: For request payloads (prevents extra fields)
- **BaseResponse**: For response models (allows ORM attribute access)
- **PaginatedResponse**: For paginated list responses

Key patterns:

- Use `Field()` with validation constraints and descriptions
- Include proper type annotations with Optional types
- Add descriptive docstrings for API documentation

### Field Validation Patterns

**Reference**: `examples/schemas/user_models.py.example` and `examples/shared/patterns.py.example` for validation examples.

#### Common Validation Patterns

- **String Validation**: min_length, max_length, pattern regex, custom validators
- **Numeric Validation**: ge (>=), gt (>), le (<=), lt (<), decimal_places
- **Date/Time Validation**: Cross-field validation with @validator decorators
- **Email Validation**: Use EmailStr type for automatic email validation
- **Custom Validation**: Use @validator and @root_validator for business rules

### Complex Model Patterns

**Reference**: `examples/schemas/user_models.py.example` for advanced model patterns.

#### Advanced Pattern Types

- **Nested Models**: Compose models within other models for complex data structures
- **Enumeration Models**: Use str/int Enums for controlled vocabulary
- **List Models**: Collections with validation on items and length
- **Dictionary Models**: Key-value pairs with type constraints
- **Generic Models**: Reusable models with type parameters

### Response Model Patterns

**Reference**: `examples/schemas/user_models.py.example` for response model examples.

#### Standard Response Types

- **Entity Responses**: Single resource with full data
- **List Responses**: Collections with metadata
- **Paginated Responses**: Use shared PaginatedResponse[T] type
- **Status Responses**: Success/error indicators with messages
- **Summary Responses**: Minimal data for references

### Model Configuration Patterns

**Reference**: `examples/shared/patterns.py.example` for configuration examples.

#### Configuration Options

- **from_attributes**: Enable ORM mode for database model conversion
- **str_strip_whitespace**: Automatically clean string inputs
- **validate_assignment**: Validate when setting attributes after creation
- **use_enum_values**: Return enum values instead of enum objects
- **Custom Serializers**: Use @field_serializer for output formatting

### Validation Error Handling

**Reference**: `examples/schemas/user_models.py.example` for validation examples.

#### Validation Strategies

- **Field Validators**: Use @validator for single field validation
- **Root Validators**: Use @root_validator for cross-field validation
- **Business Rules**: Implement domain-specific validation logic
- **Error Messages**: Provide clear, actionable error descriptions

## Model Best Practices

1. **Use descriptive model names** - End with Request/Response for clarity
2. **Inherit from base classes** - Use BaseRequest/BaseResponse appropriately
3. **Add field descriptions** - Include helpful descriptions for API documentation
4. **Use appropriate validation** - Add constraints that match business rules
5. **Keep models focused** - One model per specific use case
6. **Use type hints properly** - Leverage union types and optional fields
7. **Organize by domain** - Group related models in the same file
8. **Document complex validation** - Explain business rules in docstrings
9. **Use enums for constants** - Define allowed values as enums
10. **Test edge cases** - Consider null values, empty strings, and boundary conditions

## Reference Files

For comprehensive model examples and patterns:

- **`examples/schemas/user_models.py.example`** - Complete model examples with validation
- **`examples/shared/patterns.py.example`** - Common patterns and configuration examples

These examples demonstrate all the patterns described in this guide with working code.
