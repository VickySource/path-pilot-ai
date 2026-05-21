import type { Roadmap } from "@/types/roadmap";
import { StepCard } from "./StepCard";

export function RoadmapTimeline({ roadmap }: { roadmap: Roadmap }) {
  return (
    <ol className="space-y-3">
      {roadmap.steps.map((s, i) => (
        <StepCard key={s.id} step={s} index={i} />
      ))}
    </ol>
  );
}
