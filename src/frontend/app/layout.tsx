import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/providers";

export const metadata: Metadata = {
  title: {
    default: "PathPilot AI — Navigate your career with AI",
    template: "%s — PathPilot AI",
  },
  description:
    "AI-powered career competency navigation. Analyze skills, surface gaps, and generate personalized learning roadmaps.",
  metadataBase: new URL("https://pathpilot.ai"),
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
