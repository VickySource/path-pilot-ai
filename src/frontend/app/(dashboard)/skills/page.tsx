"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, Sparkles, Upload as UploadIcon } from "lucide-react";
import { toast } from "sonner";
import { PageHeader, EmptyState } from "@/components/common";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { GapBadge } from "@/components/roadmap/GapBadge";
import { skillsService } from "@/services/skills.service";
import { ApiError } from "@/lib/api-client";
import type { Skill, SkillGap } from "@/types/skill";

const DOC_KEY = "pathpilot.lastDocId";
const ROLE_KEY = "pathpilot.targetRole";

export default function SkillsPage() {
  const router = useRouter();
  const [docId, setDocId] = useState<string | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [gaps, setGaps] = useState<SkillGap[]>([]);
  const [role, setRole] = useState("");
  const [extracting, setExtracting] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    setDocId(window.localStorage.getItem(DOC_KEY));
    setRole(window.localStorage.getItem(ROLE_KEY) || "");
  }, []);

  async function extract() {
    if (!docId) return;
    setExtracting(true);
    try {
      const { skills } = await skillsService.extract(docId);
      setSkills(skills);
      toast.success(`Extracted ${skills.length} skills`);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Extraction failed");
    } finally {
      setExtracting(false);
    }
  }

  async function analyze() {
    if (!role.trim()) return;
    setAnalyzing(true);
    window.localStorage.setItem(ROLE_KEY, role.trim());
    try {
      const { gaps } = await skillsService.gapAnalysis(role.trim());
      setGaps(gaps);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Gap analysis failed");
    } finally {
      setAnalyzing(false);
    }
  }

  if (!docId) {
    return (
      <>
        <PageHeader title="Skill analysis" description="Extract a structured competency graph from your résumé." />
        <EmptyState
          icon={UploadIcon}
          title="No document yet"
          description="Upload your résumé to start extracting skills."
          action={<Button onClick={() => router.push("/upload")}>Go to upload</Button>}
        />
      </>
    );
  }

  return (
    <>
      <PageHeader
        title="Skill analysis"
        description="Extract skills, then compare against a target role to surface gaps."
        actions={
          <Button onClick={extract} loading={extracting} variant="secondary">
            <Sparkles className="h-3.5 w-3.5" />
            {skills.length ? "Re-extract" : "Extract skills"}
          </Button>
        }
      />

      <div className="grid gap-6 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <h3 className="mb-3 text-sm font-semibold">Extracted skills</h3>
          {skills.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No skills yet. Click <span className="font-medium text-foreground">Extract skills</span> to begin.
            </p>
          ) : (
            <ul className="flex flex-wrap gap-2">
              {skills.map((s) => (
                <li key={s.id}>
                  <Badge variant="muted" className="text-xs">
                    {s.name}
                    <span className="ml-1 text-[10px] uppercase tracking-wide text-muted-foreground">
                      {s.level}
                    </span>
                  </Badge>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card className="lg:col-span-2 space-y-3">
          <h3 className="text-sm font-semibold">Gap analysis</h3>
          <p className="text-xs text-muted-foreground">
            Compare your profile to a target role.
          </p>
          <Input
            placeholder="e.g. Senior ML Engineer"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
          <Button onClick={analyze} loading={analyzing} className="w-full" disabled={!role.trim()}>
            Run analysis
          </Button>

          {gaps.length > 0 && (
            <ul className="mt-2 space-y-2">
              {gaps.map((g, i) => (
                <li
                  key={`${g.skill.id}-${i}`}
                  className="flex items-center justify-between rounded-lg border border-border p-2.5 text-sm"
                >
                  <div>
                    <div className="font-medium">{g.skill.name}</div>
                    <div className="text-[11px] text-muted-foreground">
                      target: {g.targetLevel}
                    </div>
                  </div>
                  <GapBadge priority={g.priority} />
                </li>
              ))}
            </ul>
          )}

          {gaps.length > 0 && (
            <Button variant="outline" className="w-full" onClick={() => router.push("/roadmap")}>
              Generate roadmap <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          )}
        </Card>
      </div>
    </>
  );
}
