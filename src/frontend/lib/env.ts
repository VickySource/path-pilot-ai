import { z } from "zod";

const schema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_API_PREFIX: z.string().default("/api/v1"),
  NEXT_PUBLIC_APP_NAME: z.string().default("PathPilot AI"),
});

export const env = schema.parse({
  // Fallback keeps backwards compatibility with the older variable name.
  NEXT_PUBLIC_API_URL:
    process.env.NEXT_PUBLIC_API_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    "http://localhost:8000",
  NEXT_PUBLIC_API_PREFIX: process.env.NEXT_PUBLIC_API_PREFIX ?? "/api/v1",
  NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
});

/** Fully-qualified API base, e.g. `http://localhost:8000/api/v1`. */
export const API_BASE_URL = `${env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}${env.NEXT_PUBLIC_API_PREFIX}`;
