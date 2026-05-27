# React Frontend Project Guidelines

This document establishes the mandatory visual standards, styling patterns, state management rules, and development guidelines for the **React Web Frontend** (`frontend/`) in this repository.

---

## 1. Visual Standards & Premium Aesthetics (CRITICAL)

The UI must feel extremely premium, responsive, and alive. Do not build simple, basic, or generic layouts. Adhere to these design tokens:

### A. Color Palette & Typography
- **Harmonious HSL Colors**: Use a curated dark-mode first design system. Avoid flat `#ff0000` or plain `#0000ff`. Utilize Tailwind CSS variable-backed semantic colors (e.g. `var(--background)`, `var(--primary)`, etc.).
- **Modern Typography**: Use standard custom variable fonts like `@fontsource-variable/geist` or standard premium fonts like *Inter*, *Outfit*, or *Roboto*. Set font weights and line heights appropriately for a sleek, modern visual rhythm.
- **Glassmorphism**: Use semi-transparent background utilities with backdrops for floating menus, dialog wrappers, and sidebar interfaces (e.g. `bg-background/80 backdrop-blur-md border-border/50`).

### B. Micro-Animations & Interactivity
- **Smooth Hover States**: Every button, input field, and list item must have subtle micro-animations on interaction (e.g. `transition-all duration-300 ease-out hover:scale-[1.02] hover:shadow-lg`).
- **State Indicators**: Use pulsing status dots or glowing background gradients to denote live uploads, ongoing searches, and streaming operations.

---

## 2. Directory Structure & Organization

Code must be strictly partitioned into the following subfolders within `frontend/src/` to guarantee absolute modularity:

| Directory | Scope & Purpose |
| :--- | :--- |
| **`api/`** | TanStack React Query cache contexts, Axios API endpoints wrappers, and queries/mutations declarations. |
| **`assets/`** | Static elements including SVG vectors, local icons, background layouts, and brand logos. |
| **`components/`** | Generic visual primitives (buttons, dialogs, cards, fields). Houses shadcn/ui base primitives under `components/ui/`. |
| **`config/`** | Internationalization setups, global environment readers, and feature toggle flags. |
| **`constants/`** | Fixed text labels, external links list, API path routes, and application configuration limits. |
| **`contexts/`** | Multi-component scope systems like custom theme providers or global modal state boundaries. |
| **`enums/`** | TypeScript enum types. |
| **`features/`** | Business domain folders containing related components, hooks, and services (e.g. `auth/`, `upload/`, `search/`). |
| **`hooks/`** | Shareable, dedicated hooks abstracting specific logic (e.g., `useDebounce`, `useScrollToBottom`). |
| **`i18n/`** | Translation dictionary lists and multi-language support. |
| **`layouts/`** | Frame configurations e.g. `AuthLayout`, `WorkspaceLayout`, `Header`, or `Sidebar`. |
| **`lib/`** | Custom instances of external utility wrappers (e.g. Tailwind `cn` utility, custom vector calculations). |
| **`pages/`** | Comprehensive page containers which are mounted directly onto route contexts. |
| **`routes/`** | Navigation boundaries, public/private middleware checks, and route definitions. |
| **`schemas/`** | Validation logic schemas (e.g. Zod validation structures mapping form components). |
| **`services/`** | Modular services handling API requests, file handling, local storage storage. |
| **`stores/`** | Global state models using Zustand (e.g. search history lists, session token stores). |
| **`styles/`** | Tailwind utility setups, typography bases, and CSS variables located under `styles/global.css`. |
| **`types/`** | Shared typescript interface and type definitions. |
| **`utils/`** | Mathematical helper routines, date parsers, string formatting algorithms. |

---

## 3. Styling Guidelines & Tailwind CSS v4

The project utilizes modern **Tailwind CSS v4** bundled via `@tailwindcss/vite`.
- **Primary Style Entrypoint**: All styling is driven by `src/styles/global.css`. Do not add inline styles.
- **Predefined Classes**: Ensure components utilize Tailwind classes mapping to CSS custom variables defined in `global.css` to allow seamless dynamic theme changes.
- **Conditional Classnames**: Use the custom `cn(...)` utility (located in `src/lib/utils.ts`) to merge conditional Tailwind classes:
  ```typescript
  import { cn } from "@/lib/utils";

  export const CustomCard = ({ active }: { active: boolean }) => (
    <div className={cn(
      "p-6 rounded-xl border border-border bg-card transition-all",
      active && "border-primary shadow-[0_0_15px_rgba(var(--primary-rgb),0.15)]"
    )}>
      ...
    </div>
  );
  ```

---

## 4. State Partitioning Strategy

1. **Local State**: Keep form data, input fields, and transient toggles inside local React `useState` / `useReducer` declarations.
2. **Asynchronous/Server State**: Strictly manage network operations, endpoint fetches, and mutations caching via **TanStack React Query** under `src/api/` and `src/hooks/`.
3. **Global UI/Session State**: Manage authenticated session tokens, streaming answers lists, global workspace parameters, and sidebar toggles using **Zustand** stores inside `src/stores/`.
4. **Synchronous Prop Flow**: Prop drill no more than 3 levels deep. If data is needed deeper, use Context API or a dedicated Zustand store.

---

## 5. React 19 Standards & Conventions

- **Theme Configuration**: The Theme Provider mounts directly in `src/main.tsx` wrapping the application elements.
- **TypeScript Integration**: Avoid `any` typing under any circumstance. Define complete properties structure using TS interfaces.
- **Asynchronous Processing**: Use custom hooks for all computational routines or asynchronous API fetches to preserve thin, clean UI visual components.
