# Prompt Template: Clean Code Refactoring & Technical Debt Cleanup

Use this prompt to guide the AI in modularizing classes, cleaning code duplication, or improving system scalability.

---

## Instructions to Agent:
"Please refactor the target module inside the codebase to optimize performance, clean up redundancy, and align with SOLID principles:

### Refactoring Rules:
1. **Zero Function Alterations**: Keep public APIs, routers, schemas, and return formats completely stable unless explicitly requested.
2. **Decompose Complex Blocks**: Split large, monolithic methods into focused, single-purpose async helper functions.
3. **DRY (Don't Repeat Yourself)**: Extract duplicate operations (e.g. metadata normalization, error wrappers) into unified utility classes.
4. **Preserve Documentation**: Maintain all existant comments, JSDoc parameters, docstrings, and logger entries.

### Verification Checklist:
- Verify that TypeScript compilation passes without warnings.
- Ensure Python type validation imports (`from typing import Annotated`) remain strict.
- Confirm imports follow our Onion Architecture constraints (no Presentation layer imports inside Domain layer)."
