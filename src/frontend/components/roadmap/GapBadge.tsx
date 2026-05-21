import { cn } from "@/lib/utils";

export function GapBadge({ priority }: { priority: "low" | "medium" | "high" }) {
  const color = priority === "high" ? "bg-red-100 text-red-700" : priority === "medium" ? "bg-yellow-100 text-yellow-700" : "bg-green-100 text-green-700";
  return <span className={cn("rounded px-2 py-0.5 text-xs", color)}>{priority}</span>;
}
