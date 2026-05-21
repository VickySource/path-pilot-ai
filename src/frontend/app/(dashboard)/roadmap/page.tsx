"use client";

import { useEffect, useState } from "react";
import { Map as MapIcon, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { PageHeader, EmptyState } from "@/components/common";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { RoadmapTimeline } from "@/components/roadmap/RoadmapTimeline";
import { useRoadmap } from "@/hooks/useRoadmap";
import { ApiError } from "@/lib/api-client";

const DOC_KEY = "pathpilot.lastDocId";
const GOAL_KEY = "pathpilot.lastGoal";

export default function RoadmapPage() {
  const { roadmap, generate, loading } = useRoadmap();
  const [goal, setGoal] = useState("");
  const [docId, setDocId] = useState<string | null>(null);

  useEffect(() => {
    setDocId(window.localStorage.getItem(DOC_KEY));
    setGoal(
      window.localStorage.getItem(GOAL_KEY) ||
        window.localStorage.getItem("pathpilot.targetRole") ||
        "",
    );
  }, []);

  async function onGenerate() {
    if (!goal.trim()) return;
    window.localStorage.setItem(GOAL_KEY, goal.trim());
    try {
      await generate(goal.trim(), docId ?? undefined);
      toast.success("Roadmap generated");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Generation failed");
    }
  }

  return (
    <>
      <PageHeader
        title="Personalized roadmap"
        description="LangGraph orchestrates skill extraction, gap analysis, and roadmap generation against your résumé context."
      />

      <Card className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label className="mb-1 block text-xs font-medium text-muted-foreground">
            Target role or goal
          </label>
          <Input
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Senior ML Engineer, AI Product Manager…"
          />
        </div>
        <Button onClick={onGenerate} loading={loading} disabled={!goal.trim()}>
          <Sparkles className="h-3.5 w-3.5" />
          Generate
        </Button>
      </Card>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-28 rounded-2xl border border-border bg-card/40 animate-shimmer" />
          ))}
        </div>
      ) : roadmap ? (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold">Goal: {roadmap.goal}</h2>
            <span className="text-xs text-muted-foreground">
              {roadmap.steps.length} steps
            </span>
          </div>
          <RoadmapTimeline roadmap={roadmap} />
        </section>
      ) : (
        <EmptyState
          icon={MapIcon}
          title="No roadmap yet"
          description="Enter a target role above to generate a personalized weekly plan."
        />
      )}
    </>
  );
}
