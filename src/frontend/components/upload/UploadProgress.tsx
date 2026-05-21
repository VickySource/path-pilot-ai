export function UploadProgress({ value }: { value: number }) {
  return (
    <div className="mt-2 h-2 w-full rounded bg-gray-200">
      <div className="h-2 rounded bg-brand transition-all" style={{ width: `${value}%` }} />
    </div>
  );
}
