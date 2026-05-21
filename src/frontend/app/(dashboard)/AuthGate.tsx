"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/providers/AuthProvider";

export function AuthGate({ children }: { children: React.ReactNode }) {
  const { status } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (status === "unauthenticated") {
      const url = `/login?next=${encodeURIComponent(pathname)}`;
      router.replace(url);
    }
  }, [status, router, pathname]);

  if (status !== "authenticated") {
    return (
      <div className="grid min-h-screen place-items-center">
        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-muted-foreground border-r-transparent" />
          Loading…
        </div>
      </div>
    );
  }

  return <>{children}</>;
}