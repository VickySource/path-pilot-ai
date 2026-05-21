import { apiClient } from "@/lib/api-client";
import type { Roadmap } from "@/types/roadmap";

export const roadmapService = {
  generate: (goal: string, documentId?: string) =>
    apiClient.post<Roadmap>("/roadmap/generate", { goal, documentId }).then((r) => r.data),
  get: (id: string) => apiClient.get<Roadmap>(`/roadmap/${id}`).then((r) => r.data),
  list: () => apiClient.get<Roadmap[]>("/roadmap").then((r) => r.data),
};
