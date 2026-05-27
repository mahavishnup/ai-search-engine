# 🧭 Git Workflow & Contribution Guide

## 📌 Overview

This repository follows a strict, enterprise-ready **Fork → Branch → Pull Request (PR)** workflow.

**🚫 Never push directly** to the `main` or `develop` branches.  
All changes must go through **Pull Requests** with proper descriptions, complete unit test coverage, and linting passes.

---

## 🏗️ Workflow Summary

1. **Fork the repository** (only once per developer)
2. **Clone your fork** locally to your workspace
3. **Create a feature/bugfix branch** from `develop`
4. **Make your changes** and commit using **Conventional Commits** (`feat(scope): description`)
5. **Format and test** your code locally before pushing (runs linters, test runner suites)
6. **Push your branch** to your fork origin
7. **Open a Pull Request (PR)** → from your branch **into the main repo `develop` branch**
8. **Get review approval** (at least 1-2 approvals) and ensure CI/CD builds pass before merging

---

## 🏷️ Conventional Commits Standard

We enforce a strict conventional commit format to maintain a clean, readable, and machine-parsable history.

### Commit Format
```text
<type>(<scope>): <description>

[optional body describing the 'why' and structural changes]

[optional footer referencing issue numbers, e.g., Closes #123]
```

### Types & Scopes
* **`feat`**: A new user-facing feature or API endpoint.
* **`fix`**: A bug fix (e.g., correcting an index out-of-bounds, fixing a redirect logic).
* **`docs`**: Documentation-only changes (e.g., updating ARCHITECTURE.md).
* **`style`**: Changes that do not affect code execution (white-space, formatting, missing semi-colons).
* **`refactor`**: A code change that neither fixes a bug nor adds a feature, but improves code structure.
* **`perf`**: A code change that improves execution speed or memory efficiency.
* **`test`**: Adding missing tests or correcting existing tests.
* **`build` / `chore`**: Changes that affect the build system, package updates, or dev tools configuration.

### Examples of Good Commit Messages
* `feat(api): add async registration and user login controllers`
* `feat(ui): add glassmorphic dashboard layout with glowing scrollbars`
* `fix(vector): correct FAISS file-flush locks on Windows filesystems`
* `test(frontend): verify env schema validation via Vitest`
* `docs(readme): update prerequisite stack and local setup instructions`
* `chore(deps): upgrade Pydantic to 2.10.x`

---

## ⚙️ Command Flow Reference

### 1. Fork and Clone
- Click the **Fork** button on the top-right of the main GitHub repository.
- Clone your fork locally:
```bash
git clone https://github.com/<your-username>/ai-search-engine.git
cd ai-search-engine
```

### 2. Configure Upstream
Keep your local repository connected to the parent repository to pull the latest changes:
```bash
git remote add upstream https://github.com/mahavishnup/ai-search-engine.git
```

Verify your remotes:
```bash
git remote -v
```

### 3. Sync and Start Working
Before starting any new coding task, always sync with the upstream parent branch:
```bash
git fetch upstream
git checkout develop
git pull upstream develop
git push origin develop
```

Create a new branch from `develop`:
```bash
git checkout -b feat/api-user-auth  # for features
# or
git checkout -b fix/vector-leak     # for bugfixes
```

### 4. Make Changes & Local Verification
Ensure your code is perfectly formatted, passes linters, and completes all automated tests before committing.

**Backend Checks:**
```bash
cd backend
source .venv/Scripts/activate # Windows Git Bash
black src                     # Code Formatter
pytest                        # Test Runner
```

**Frontend Checks:**
```bash
cd frontend
npm run format                # Run Prettier code formatter
npm run lint                  # Run ESLint validation
npm run test                  # Run Vitest unit tests
npm run build                 # Verify production compilation
```

### 5. Commit and Push
Create your commit using conventional commits style:
```bash
git add .
git commit -m "feat(api): add user registration and JWT authentication endpoints"
```
Push the branch to your fork:
```bash
git push origin feat/api-user-auth
```

### 6. Create the Pull Request (PR)
- Go to your fork on GitHub.
- Click **Compare & Pull Request**.
- Set base repository to **mahavishnup/ai-search-engine → `develop`**.
- Set compare branch to **`<your-username>:feat/api-user-auth`**.

---

## 📝 Pull Request Guidelines

### PR Title Format
Follow the conventional commits styling, capitalized as a short summary:
* `[feat-api] Add JWT token authentication`
* `[fix-vector] Correct FAISS segment flush locks`
* `[docs] Update scaffolding directories and meanings`

### PR Description Template
```markdown
## Summary
Briefly describe what this PR accomplishes and its architectural approach.

## Proposed Changes
- Created auth routes `/auth/register` and `/auth/login`
- Developed SQL password hashing repository helpers in domain layer
- Created Zustand state managers and wired React guarded route paths

## Test Scenarios & Results
- [x] Passed pytest suite verifying authentication routes response codes
- [x] Verified Vitest client environment Zod validation schemes
- [x] Checked production build compilation outputs

## Related Issues
Closes #XX
```

---

## 🚀 Release Delivery Protocol
Once features are thoroughly tested in `develop`, a deployment release is cut:
1. Merge `develop` into `main`.
2. Apply an annotated semantic version tag:
```bash
git checkout main
git pull upstream main
git merge develop
git tag -a v1.0.0 -m "Release Version 1.0.0 (Phase 1 Baseline)"
git push upstream main --tags
```
