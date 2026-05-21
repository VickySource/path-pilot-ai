import { apiClient } from "@/lib/api-client";
import type { User } from "@/types/user";

export const authService = {
  login: (email: string, password: string) =>
    apiClient.post<{ access_token: string; user: User }>("/auth/login", { email, password }).then((r) => r.data),
  register: (email: string, password: string, name: string) =>
    apiClient.post<{ user: User }>("/auth/register", { email, password, name }).then((r) => r.data),
  me: () => apiClient.get<User>("/auth/me").then((r) => r.data),
};
