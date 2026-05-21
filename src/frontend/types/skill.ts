export interface Skill {
  id: string;
  name: string;
  level: "beginner" | "intermediate" | "advanced" | "expert";
  category?: string;
}

export interface SkillGap {
  skill: Skill;
  targetLevel: Skill["level"];
  priority: "low" | "medium" | "high";
}
