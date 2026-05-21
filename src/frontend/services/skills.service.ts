import { apiClient } from "@/lib/api-client";
import type { Skill, SkillGap } from "@/types/skill";

export const skillsService = {
  extract: (documentId: string) =>
    apiClient.post<{ skills: Skill[] }>("/skills/extract", { documentId }).then((r) => r.data),
  gapAnalysis: (targetRole: string) =>
    apiClient.post<{ gaps: SkillGap[] }>("/skills/gap-analysis", { targetRole }).then((r) => r.data),
};
