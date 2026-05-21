import { DashboardShell } from "@/components/layout/DashboardShell";
import { AuthGate } from "./AuthGate";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthGate>
      <DashboardShell>{children}</DashboardShell>
    </AuthGate>
  );
}
