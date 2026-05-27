# Prompt Template: Automated Unit & Integration Testing

Use this prompt to guide the AI when writing robust test coverage for backend and frontend domains.

---

## Instructions to Agent:
"Please design and build high-coverage tests for the target module:

### Backend Testing (pytest + pytest-asyncio):
- Write tests inside the 'tests/' directory.
- Utilize async database transaction fixtures with mock sessions or temporary sqlite/postgres engines.
- Verify edge cases:
  - Valid and invalid input payloads (verifying Pydantic raises correct validation errors).
  - Internal database exception blocks (verifying correct rollbacks).
  - External API timeouts (using mock wrappers).
- Ensure all test methods use strict assertions.

### Frontend Testing (React Testing Library / Vitest / Jest):
- Build modular test blocks mapping component behaviors.
- Mock global Zustand stores cleanly, checking state boundaries.
- Test active states (loading spinners, text changes, button triggers)."
