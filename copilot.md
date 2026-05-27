# copilot.md — GitHub Copilot Developer Instructions & Prompts

You are operating as **GitHub Copilot**, the inline autocomplete, boilerplate generation, and syntax velocity specialist for the **AI Semantic Search Engine** project.

---

## ⚡ TOKEN OPTIMIZATION & LAZY-LOADING PROTOCOL

> [!IMPORTANT]
> **DO NOT parse or load the entire guideline library on initialization.**
> To optimize token usage, minimize completion latency, and keep suggestions fast, load rules **lazily on-demand**:
>
> - **When writing React 19 Frontend components**: Read [.github/instructions/react-project-guidelines.md](.github/instructions/react-project-guidelines.md) & [premium-react-development](.github/skills/premium-react-development/SKILL.md)
> - **When coding FastAPI Backend routes/schemas**: Read [.github/instructions/python.instructions.md](.github/instructions/python.instructions.md) & [backend-onion-development](.github/skills/backend-onion-development/SKILL.md)
>
> Focus strictly on inline completion speed, semantic syntax safety, and localized typing.

---

## 🧭 Core Strengths
- **Instant Boilerplate**: Quick generation of SQLAlchemy 2.0 ORM schemas, application schemas (Pydantic), and Zustand actions.
- **Visual Scaffolding**: Fast Tailwind CSS v4 class setups matching our premium glassmorphic theme rules.

---

## 🛠️ Context-Based Copilot Prompts

### A. Async Repository Scaffolding (Inline Trigger)
```text
Scaffold a complete asynchronous repository wrapper for the [ModelName] entity in 'infrastructure/repositories/[name]_repository.py' following these standards:
- Inherit from '[InterfaceName]' and inject database session via: Annotated[AsyncSession, Depends(get_session)]
- Implement CRUD operations using SQLAlchemy 2.0 async select/insert/update syntax.
- Wrap modifications in try/except with clean rollbacks.
```

### B. Premium UI React Component (Inline Trigger)
```text
Create a reusable, premium glassmorphic SearchBar React 19 component inside 'components/SearchBar.tsx':
- Declare strict TypeScript interfaces for all props.
- Style with Tailwind CSS v4: bg-background/80 backdrop-blur border border-border/50 hover:border-primary/50 focus-within:ring-2.
- Apply dynamic hover transitions (transition-all duration-300 hover:scale-[1.01]).
```
