"use client";
import { useState } from "react";
import { roadmapService } from "@/services/roadmap.service";
import type { Roadmap } from "@/types/roadmap";

export function useRoadmap() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(false);

  async function generate(goal: string, documentId?: string) {
    setLoading(true);
    try {
      const r = await roadmapService.generate(goal, documentId);
      setRoadmap(r);
      return r;
    } finally {
      setLoading(false);
    }
  }

  return { roadmap, generate, loading };
}
