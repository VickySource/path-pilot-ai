import Link from "next/link";
import { ArrowRight, Brain, Compass, Sparkles } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Skill intelligence",
    body: "Upload a résumé and let local LLMs extract a structured competency graph.",
  },
  {
    icon: Compass,
    title: "Gap analysis",
    body: "Compare your profile against any target role and see what's missing — instantly.",
  },
  {
    icon: Sparkles,
    title: "Personal roadmaps",
    body: "LangGraph-orchestrated workflows turn gaps into a week-by-week learning plan.",
  },
];

export default function LandingPage() {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-grid opacity-40 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]" />
      <div className="relative mx-auto flex max-w-5xl flex-col items-center gap-10 px-6 py-24 text-center">
        <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card/60 px-3 py-1 text-xs font-medium text-muted-foreground backdrop-blur">
          <Sparkles className="h-3.5 w-3.5 text-primary" />
          Local LLMs · RAG · LangGraph
        </span>
        <h1 className="text-balance text-5xl font-semibold tracking-tight sm:text-6xl">
          Navigate your career with{" "}
          <span className="bg-gradient-to-r from-primary to-accent-foreground bg-clip-text text-transparent">
            AI clarity
          </span>
          .
        </h1>
        <p className="max-w-2xl text-balance text-lg text-muted-foreground">
          PathPilot AI analyzes your skills, identifies competency gaps, and generates
          personalized learning roadmaps — privately, on your own infrastructure.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/login"
            className="inline-flex items-center gap-2 rounded-full bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow-sm transition hover:opacity-90"
          >
            Get started <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-5 py-2.5 text-sm font-medium transition hover:bg-muted"
          >
            Create account
          </Link>
        </div>

        <section className="mt-16 grid w-full gap-4 sm:grid-cols-3">
          {features.map(({ icon: Icon, title, body }) => (
            <article
              key={title}
              className="group rounded-2xl border border-border bg-card/60 p-6 text-left backdrop-blur transition hover:border-primary/40 hover:bg-card"
            >
              <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-accent text-accent-foreground">
                <Icon className="h-4.5 w-4.5" />
              </div>
              <h3 className="text-sm font-semibold">{title}</h3>
              <p className="mt-1 text-sm text-muted-foreground">{body}</p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
