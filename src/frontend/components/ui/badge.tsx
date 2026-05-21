import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

type Variant = "default" | "muted" | "success" | "warning" | "destructive" | "outline";

const VARIANTS: Record<Variant, string> = {
  default: "bg-primary/10 text-primary border-primary/20",
  muted: "bg-muted text-muted-foreground border-transparent",
  success: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  warning: "bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400",
  destructive: "bg-destructive/10 text-destructive border-destructive/20",
  outline: "border-border text-foreground",
};

export function Badge({
  className,
  variant = "default",
  ...props
}: HTMLAttributes<HTMLSpanElement> & { variant?: Variant }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-medium",
        VARIANTS[variant],
        className,
      )}
      {...props}
    />
  );
}