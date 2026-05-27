# copilot-instructions.md — GitHub Copilot Operational Instructions

You are operating as **GitHub Copilot**, the inline autocomplete, boilerplate generation, and syntax velocity specialist for the **AI Semantic Search Engine** project.

---

## ⚡ TOKEN OPTIMIZATION & LAZY-LOADING PROTOCOL

> [!IMPORTANT]
> **DO NOT parse or load the entire architectural guidelines suite on initialization.**
> To minimize completion latency and preserve token efficiency, load sub-rules **lazily on-demand**:
>
> - **When writing React 19 Frontend components**: Read [.cursor/rules/frontend.mdc](../.cursor/rules/frontend.mdc) & [premium-react-development](../skills/premium-react-development/SKILL.md)
> - **When coding FastAPI Backend routes/schemas**: Read [.cursor/rules/backend.mdc](../.cursor/rules/backend.mdc) & [backend-onion-development](../skills/backend-onion-development/SKILL.md)
> - **PR Review Compliance**: Read [pull_request_template.md](pull_request_template.md) only when finalizing commits.
>
> Focus strictly on inline completion speed, local typing accuracy, and matching existing coding patterns in sibling files.

---

## 🧭 Core Autocomplete Directives
- **Zero Disruptions**: Preserve all JSDoc blocks, python docstrings, existant logs, and helper methods.
- **Strict Typing**: Generate strict typescript interfaces and annotated python type declarations. Avoid `any` mapping or untyped API routes.
- **Zero Placeholders**: Do not write comments like `// TODO: Implement later` or `pass` in production directories.
