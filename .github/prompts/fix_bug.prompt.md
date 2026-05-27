# Prompt Template: Surgical Bug Fixing & Diagnostics

Use this prompt to guide an AI agent when troubleshooting, debugging, or solving structural failures.

---

## Instructions to Agent:
"We are encountering an anomaly or error in the application. Please perform a surgical diagnostic analysis and implement a clean fix:

### Step 1: Context Research & Investigation
- Use ripgrep (`grep_search`) to locate references to the failing functions, variables, or API routes.
- View related files to understand the surrounding context, import paths, and async lifecycles.
- Locate the related logging or error handler files to see how the system captures errors.

### Step 2: Formulate the Clean Fix
- Focus on root causes (e.g., SQLAlchemy session race conditions, unhandled exceptions, incorrect TypeScript prop maps).
- Implement a focused, targeted fix. Avoid modifying code blocks unrelated to the issue.
- Ensure all types are strictly updated and no standard behaviors are broken.

### Step 3: Verify and Secure
- Double-check that session management uses clean rollback blocks.
- Confirm imports are structured cleanly and do not introduce circular chains.
- Provide a summary explaining:
  1. What was the root cause.
  2. How you solved it.
  3. Any side effects you verified."
