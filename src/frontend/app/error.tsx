"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="grid min-h-screen place-items-center px-6 text-center">
      <div>
        <p className="text-xs font-medium uppercase tracking-wider text-destructive">
          Something went wrong
        </p>
        <h1 className="mt-2 text-2xl font-semibold tracking-tight">
          We hit an unexpected error
        </h1>
        <p className="mt-2 max-w-md text-sm text-muted-foreground">
          {error.message || "Please try again. If the problem persists, contact support."}
        </p>
        <button
          onClick={reset}
          className="mt-6 inline-flex rounded-full bg-primary px-5 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
        >
          Try again
        </button>
      </div>
    </main>
  );
}
