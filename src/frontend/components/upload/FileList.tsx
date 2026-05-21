export function FileList({ files }: { files: { name: string; size: number }[] }) {
  return (
    <ul className="mt-4 space-y-1 text-sm">
      {files.map((f) => (
        <li key={f.name}>{f.name} — {(f.size / 1024).toFixed(1)} KB</li>
      ))}
    </ul>
  );
}
