"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Sparkles,
  Map as MapIcon,
  Upload,
  MessageSquare,
  BarChart3,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

type NavItem = { href: string; label: string; icon: LucideIcon };

export const NAV: NavItem[] = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/skills", label: "Skills", icon: Sparkles },
  { href: "/roadmap", label: "Roadmap", icon: MapIcon },
  { href: "/upload", label: "Upload", icon: Upload },
  { href: "/chat", label: "AI Chat", icon: MessageSquare },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export function SidebarContent({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();

  return (
    <div className="flex h-full flex-col px-3 py-5">
      <Link
        href="/dashboard"
        onClick={onNavigate}
        className="mb-8 flex items-center gap-2 px-2"
      >
        <span className="grid h-8 w-8 place-items-center rounded-xl bg-gradient-to-br from-primary to-accent-foreground text-primary-foreground shadow-sm">
          <Sparkles className="h-4 w-4" />
        </span>
        <span className="text-sm font-semibold tracking-tight">PathPilot AI</span>
      </Link>

      <nav className="flex flex-col gap-0.5">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname === href || pathname?.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              onClick={onNavigate}
              className={cn(
                "group relative flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                active
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <Icon className={cn("h-4 w-4 transition", active && "text-primary")} />
              {label}
              {active && (
                <span className="absolute right-3 h-1 w-1 rounded-full bg-primary" />
              )}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto rounded-xl border border-border bg-card/60 p-3 text-xs text-muted-foreground">
        Running on local LLMs — your data never leaves your infra.
      </div>
    </div>
  );
}

export function Sidebar() {
  return (
    <aside className="hidden w-60 shrink-0 border-r border-border bg-card/40 md:flex md:flex-col">
      <SidebarContent />
    </aside>
  );
}
