import type { RoadmapStep } from "@/types/roadmap";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, ExternalLink } from "lucide-react";

export function StepCard({ step, index }: { step: RoadmapStep; index?: number }) {
  return (
    <Card className="space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          {typeof index === "number" && (
            <span className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-accent text-xs font-semibold text-accent-foreground">
              {index + 1}
            </span>
          )}
          <div>
            <div className="font-semibold">{step.title}</div>
            <p className="mt-1 text-sm text-muted-foreground">{step.description}</p>
          </div>
        </div>
        <Badge variant="muted" className="shrink-0">
          <Clock className="h-3 w-3" />~{step.estimatedHours}h
        </Badge>
      </div>

      {step.skills?.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {step.skills.map((s) => (
            <Badge key={s.id} variant="default">{s.name}</Badge>
          ))}
        </div>
      )}

      {step.resources?.length > 0 && (
        <ul className="space-y-1 border-t border-border pt-3 text-sm">
          {step.resources.map((r) => (
            <li key={r.url}>
              <a
                href={r.url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 text-primary hover:underline"
              >
                <ExternalLink className="h-3 w-3" />
                {r.title}
              </a>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
