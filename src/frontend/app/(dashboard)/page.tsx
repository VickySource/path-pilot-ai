"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Map as MapIcon, MessageSquare, Sparkles, Upload } from "lucide-react";
import { KpiCard } from "@/components/dashboard/KpiCard";
import { ProgressWidget } from "@/components/dashboard/ProgressWidget";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/common";
import { useAuth } from "@/providers/AuthProvider";
import { analyticsService } from "@/services/analytics.service";

const QUICK = [
  { href: "/upload", label: "Upload résumé", icon: Upload },
  { href: "/skills", label: "Extract skills", icon: Sparkles },
  { href: "/roadmap", label: "Generate roadmap", icon: MapIcon },
  { href: "/chat", label: "Ask the coach", icon: MessageSquare },
];

export default function DashboardHome() {
  const { user } = useAuth();
  const { data } = useQuery({
    queryKey: ["analytics-summary"],
    queryFn: analyticsService.summary,
    retry: false,
  });

  const totalSteps = data?.totalSteps ?? 0;
  const completed = data?.completedSteps ?? 0;
  const pct = totalSteps ? Math.round((completed / totalSteps) * 100) : 0;

  return (
    <>
      <PageHeader
        title={`Welcome back${user?.name ? `, ${user.name.split(" ")[0]}` : ""}`}
        description="A snapshot of your career navigation progress, powered by local LLMs."
      />

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Skills identified" value={data?.totalSkills ?? "—"} icon={Sparkles} />
        <KpiCard label="Roadmap steps" value={totalSteps || "—"} icon={MapIcon} />
        <KpiCard label="Completed" value={completed || "—"} icon={Upload} />
        <KpiCard label="Progress" value={totalSteps ? `${pct}%` : "—"} icon={MessageSquare} />
      </section>

      <section className="mt-8 grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Roadmap progress</CardTitle>
            <span className="text-xs text-muted-foreground">cumulative</span>
          </CardHeader>
          <ProgressWidget value={pct} />
          <p className="mt-3 text-sm text-muted-foreground">
            {totalSteps
              ? `${completed} of ${totalSteps} steps complete. Keep going.`
              : "Generate a roadmap to start tracking your weekly learning milestones."}
          </p>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick actions</CardTitle>
          </CardHeader>
          <ul className="space-y-1">
            {QUICK.map(({ href, label, icon: Icon }) => (
              <li key={href}>
                <Link
                  href={href}
                  className="group flex items-center justify-between rounded-lg px-2 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
                >
                  <span className="inline-flex items-center gap-2">
                    <Icon className="h-3.5 w-3.5" />
                    {label}
                  </span>
                  <ArrowRight className="h-3.5 w-3.5 opacity-0 transition group-hover:opacity-100" />
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      </section>
    </>
  );
}
