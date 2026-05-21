# Frontend conventions

- **App Router** with route groups: `(auth)` and `(dashboard)`.
- **`services/`** is the *only* place that calls the backend. Components and hooks consume services — never call `apiClient` directly from a component.
- **`lib/api-client.ts`** centralizes base URL, auth header injection, and error normalization.
- **`types/`** mirrors backend Pydantic schemas.
- **`hooks/`** wraps services with React state. Prefer adding TanStack Query later for caching.
- **Auth-ready**: token storage in `lib/auth.ts`; swap to httpOnly cookies + a real auth provider (NextAuth/Clerk) when ready.

## Adding a new feature

1. Add types in `types/<feature>.ts`.
2. Add a service in `services/<feature>.service.ts`.
3. Add a hook in `hooks/use<Feature>.ts`.
4. Add UI under `app/(dashboard)/<feature>/page.tsx` and components under `components/<feature>/`.
