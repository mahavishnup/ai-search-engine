import { cn } from "@/lib/utils"

export function App() {
  return (
    <main
      className={cn(
        "min-h-screen bg-background text-foreground",
        "flex items-center justify-center px-6 py-12"
      )}
    >
      <div className="w-full max-w-3xl rounded-[2rem] border border-border bg-card/95 p-10 shadow-2xl shadow-black/10 backdrop-blur-xl">
        <h1 className="text-4xl font-semibold tracking-tight">
          AI Semantic Search Engine
        </h1>
        <p className="mt-4 text-base leading-7 text-muted-foreground">
          Phase 1 bootstrap is partially implemented. The frontend shell is
          active and the backend is prepared for API routing.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-3xl border border-border/70 bg-background/70 p-5 shadow-sm">
            <p className="text-sm font-medium tracking-[0.24em] text-muted-foreground uppercase">
              Frontend
            </p>
            <p className="mt-2 text-sm">
              Theme provider, global styles, and application shell are
              scaffolded.
            </p>
          </div>
          <div className="rounded-3xl border border-border/70 bg-background/70 p-5 shadow-sm">
            <p className="text-sm font-medium tracking-[0.24em] text-muted-foreground uppercase">
              Backend
            </p>
            <p className="mt-2 text-sm">
              FastAPI app, health route, exception handlers, and config are now
              bootstrapped.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
