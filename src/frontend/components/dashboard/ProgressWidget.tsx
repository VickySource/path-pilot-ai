export function ProgressWidget({ value, max = 100 }: { value: number; max?: number }) {
  const pct = Math.min(100, Math.round((value / max) * 100));
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-gradient-to-r from-primary to-accent-foreground transition-all"
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}
