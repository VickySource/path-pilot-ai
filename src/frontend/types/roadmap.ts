import type { Skill } from "./skill";

export interface RoadmapStep {
  id: string;
  title: string;
  description: string;
  estimatedHours: number;
  resources: { title: string; url: string }[];
  skills: Skill[];
}

export interface Roadmap {
  id: string;
  userId: string;
  goal: string;
  steps: RoadmapStep[];
  createdAt: string;
}
