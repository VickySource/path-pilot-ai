"use client";

import { Toaster } from "sonner";
import { AuthProvider } from "./AuthProvider";
import { QueryProvider } from "./QueryProvider";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryProvider>
      <AuthProvider>
        {children}
        <Toaster
          position="bottom-right"
          theme="system"
          toastOptions={{
            className:
              "!bg-card !text-card-foreground !border !border-border !rounded-xl",
          }}
        />
      </AuthProvider>
    </QueryProvider>
  );
}