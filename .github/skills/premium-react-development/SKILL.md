---
name: premium-react-development
description: Activates when coding frontend components. Enforces Tailwind CSS v4 variables, Zustand setups, TypeScript interfaces, and premium glassmorphic visual aesthetics.
---

# Skill: Premium React Development

This skill provides full design and operational guidelines for styling and structuring feature views in the frontend.

---

## 💅 Glassmorphic UI Aesthetics Spec

Ensure all panels, headers, and dashboard widgets adhere to these specifications:
- **Base Style**: Semi-transparent dark overlay with background blurring:
  `bg-neutral-950/80 backdrop-blur-md border border-white/5`
- **Dynamic Borders**: Clean accent edges highlighting on user focus/hover:
  `transition-all duration-300 hover:border-violet-500/30 hover:shadow-violet-950/10`
- **Zero Raw Color Codes**: Always extract CSS coloring values from themes in `src/styles/global.css`.

---

## ⚙️ Zustand Store Selector Rules

To prevent performance lagging and excess React 19 re-renders:
- Always read properties selectively rather than mapping the entire store object:
  ```typescript
  const activeQuery = useSearchStore((state) => state.activeQuery);
  ```
- Declare explicit TypeScript Interfaces mapping every store action parameter.
