---
applyTo: "**/*.{ts,tsx,js,jsx}"
---

# Project coding standards for React/TypeScript

## General Code Style

- Follow consistent TypeScript/JavaScript conventions and best practices.
- Always prioritize readability, maintainability, and clarity.
- Use TypeScript for type safety; avoid `any` type unless absolutely necessary.
- Use functional components with hooks instead of class components.
- Maintain proper indentation (2 spaces per level).
- Use ESLint and Prettier for linting and formatting. Configuration is in `.eslintrc` and `.prettierrc`.

## Component Guidelines

- Write clear and descriptive names for components using PascalCase (e.g., `UserProfile`, `NavigationBar`).
- Keep components small and focused on a single responsibility.
- Extract reusable logic into custom hooks (prefix with `use`, e.g., `useAuth`, `useFetch`).
- Use meaningful prop names and always define PropTypes or TypeScript interfaces for props.
- Prefer composition over inheritance.
- Use named exports for components unless there's a specific reason for default exports.

## React Best Practices

- Use destructuring for props and state to improve readability.
- Implement proper error boundaries for production-grade applications.
- Optimize performance with `React.memo`, `useMemo`, and `useCallback` when necessary.
- Avoid inline function definitions in JSX that could cause unnecessary re-renders.
- Use fragment (`<>...</>`) instead of unnecessary wrapper divs.
- Keep business logic separate from UI components.

## State Management

- Use `useState` for local component state.
- Use `useReducer` for complex state logic.
- Consider Context API for shared state across multiple components.
- Keep state as close to where it's used as possible.
- Avoid prop drilling; use context or state management libraries when appropriate.

## TypeScript Conventions

- Define interfaces or types for all props, state, and complex objects.
- Use `interface` for object shapes and `type` for unions, intersections, or primitives.
- Place type definitions in separate files when shared across multiple components.
- Use strict mode TypeScript configuration.

## Documentation

- Write JSDoc comments for complex functions and custom hooks.
- Include comments for non-obvious logic or business rules.
- Document component props with descriptions in TypeScript interfaces.

## File Organization

- One component per file (except for small, tightly coupled sub-components).
- Use index files for cleaner imports when appropriate.
- Group related files (component, styles, tests) in the same directory.
- Follow consistent naming: `ComponentName.tsx`, `ComponentName.module.css`, `ComponentName.test.tsx`.

## Styling

- Use CSS Modules, Styled Components, or Tailwind CSS consistently across the project.
- Avoid inline styles except for dynamic styling based on props/state.
- Keep style definitions close to their components.

## Testing

- Write unit tests for components using React Testing Library.
- Test user interactions and component behavior, not implementation details.
- Aim for meaningful test coverage on critical paths.
