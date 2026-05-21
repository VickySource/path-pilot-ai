import { apiClient } from "@/lib/api-client";

export interface AnalyticsSummary {
  totalSkills: number;
  completedSteps: number;
  totalSteps: number;
  trend: { date: string; value: number }[];
}

export const analyticsService = {
  summary: () => apiClient.get<AnalyticsSummary>("/analytics/summary").then((r) => r.data),
};
