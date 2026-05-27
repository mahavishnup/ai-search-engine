# Prompt Template: Create Premium UI Component (React 19)

Use this prompt to guide the AI when engineering atomic React components, layouts, or feature views.

---

## Instructions to Agent:
"Please design and code a premium, responsive React component under 'frontend/src/components/' or 'frontend/src/features/':

### Visual Aesthetics Specifications (Mandatory):
- **Glassmorphism Base**: Leverage transparent backgrounds with backdrop filters: `bg-background/80 backdrop-blur-md border border-border/40`.
- **Dynamic Accent Borders**: Incorporate clean border indicators that react to user inputs: `focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/20`.
- **Sleek Gradients**: Use curated gradients for highlights (e.g. `bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500`).
- **Interactive Transitions**: Apply smooth micro-animations for hover, focus, and state flips: `transition-all duration-300 hover:scale-[1.01] hover:shadow-lg`.
- **Zero Raw Color Codes**: Always pull themes and hues from Tailwind variables managed inside 'src/styles/global.css'.

### Coding Integrity:
- Declare strict, complete TypeScript Interfaces mapping all component props.
- Leverage lucide-react for modern icons.
- Ensure the component is fully responsive and accessible (aria tags where interactive)."
