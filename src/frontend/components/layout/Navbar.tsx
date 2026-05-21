"use client";

import { usePathname } from "next/navigation";
import { useState } from "react";
import { LogOut, Menu, X } from "lucide-react";
import { useAuth } from "@/providers/AuthProvider";
import { Button } from "@/components/ui/button";
import { SidebarContent } from "./Sidebar";

const TITLES: Record<string, string> = {
  "/dashboard": "Overview",
  "/skills": "Skills",
  "/roadmap": "Roadmap",
  "/upload": "Upload",
  "/chat": "AI Chat",
  "/analytics": "Analytics",
};

function initials(name?: string | null) {
  if (!name) return "·";
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase())
    .join("");
}

export function Navbar() {
  const pathname = usePathname() ?? "/dashboard";
  const key = Object.keys(TITLES).find((k) => pathname.startsWith(k)) ?? "/dashboard";
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-20 flex h-14 items-center justify-between border-b border-border bg-background/70 px-4 sm:px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <Button
            size="icon"
            variant="ghost"
            className="md:hidden"
            onClick={() => setMobileOpen(true)}
            aria-label="Open navigation"
          >
            <Menu className="h-4 w-4" />
          </Button>
          <div>
            <div className="text-[11px] uppercase tracking-wider text-muted-foreground">
              Career navigation
            </div>
            <div className="text-sm font-medium">{TITLES[key] ?? "Dashboard"}</div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="hidden items-center gap-2 rounded-full border border-border bg-card/60 py-1 pl-1 pr-3 sm:flex">
            <span className="grid h-7 w-7 place-items-center rounded-full bg-accent text-[11px] font-semibold text-accent-foreground">
              {initials(user?.name || user?.email)}
            </span>
            <div className="leading-tight">
              <div className="text-xs font-medium">{user?.name || "You"}</div>
              <div className="text-[10px] text-muted-foreground">{user?.email}</div>
            </div>
          </div>
          <Button size="icon" variant="ghost" onClick={logout} aria-label="Sign out" title="Sign out">
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </header>

      {mobileOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div
            className="absolute inset-0 bg-background/70 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <div className="absolute left-0 top-0 h-full w-64 border-r border-border bg-card animate-fade-up">
            <div className="flex justify-end p-2">
              <Button size="icon" variant="ghost" onClick={() => setMobileOpen(false)} aria-label="Close">
                <X className="h-4 w-4" />
              </Button>
            </div>
            <SidebarContent onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
}
