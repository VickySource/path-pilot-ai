"use client";

import { useQuery } from "@tanstack/react-query";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { BarChart3, MessageSquare, Sparkles, Target } from "lucide-react";
import { PageHeader, EmptyState } from "@/components/common";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { KpiCard } from "@/components/dashboard/KpiCard";
import { analyticsService } from "@/services/analytics.service";

export default function AnalyticsPage() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["analytics-summary"],
    queryFn: analyticsService.summary,
  });

  if (isLoading) {
    return (
      <>
        <PageHeader title="Analytics" description="Track your learning velocity and engagement." />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-24 rounded-2xl border border-border bg-card/40 animate-shimmer" />
          ))}
        </div>
      </>
    );
  }

  if (isError || !data) {
    return (
      <>
        <PageHeader title="Analytics" />
        <EmptyState
          icon={BarChart3}
          title="Could not load analytics"
          description="The backend may not be running. Start FastAPI on http://localhost:8000 and try again."
          action={
            <button
              onClick={() => refetch()}
              className="rounded-lg bg-primary px-3 py-2 text-sm font-medium text-primary-foreground"
            >
              Retry
            </button>
          }
        />
      </>
    );
  }

  const pct = data.totalSteps
    ? Math.round((data.completedSteps / data.totalSteps) * 100)
    : 0;

  return (
    <>
      <PageHeader title="Analytics" description="Track your learning velocity and engagement." />

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Skills" value={data.totalSkills} icon={Sparkles} />
        <KpiCard label="Steps completed" value={`${data.completedSteps}/${data.totalSteps}`} icon={Target} />
        <KpiCard label="Roadmap progress" value={`${pct}%`} icon={BarChart3} />
        <KpiCard
          label="Sessions"
          value={data.trend?.length ?? 0}
          icon={MessageSquare}
        />
      </section>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Engagement trend</CardTitle>
          <span className="text-xs text-muted-foreground">last 30 days</span>
        </CardHeader>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.trend || []}>
              <defs>
                <linearGradient id="ppArea" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={0.5} />
                  <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={11} />
              <YAxis stroke="hsl(var(--muted-foreground))" fontSize={11} />
              <Tooltip
                contentStyle={{
                  background: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                fill="url(#ppArea)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </>
  );
}
