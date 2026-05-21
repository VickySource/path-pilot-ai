// TODO: replace with a proper modal library or implementation
export function Dialog({ open, children }: { open: boolean; children: React.ReactNode }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40">
      <div className="rounded bg-white p-6 shadow-lg">{children}</div>
    </div>
  );
}
