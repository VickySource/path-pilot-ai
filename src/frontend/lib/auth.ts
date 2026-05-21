const TOKEN_KEY = "pathpilot.token";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 7; // 7 days

function writeCookie(value: string | null) {
  if (typeof document === "undefined") return;
  if (value) {
    document.cookie = `${TOKEN_KEY}=${encodeURIComponent(value)}; path=/; max-age=${COOKIE_MAX_AGE}; samesite=lax`;
  } else {
    document.cookie = `${TOKEN_KEY}=; path=/; max-age=0; samesite=lax`;
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(TOKEN_KEY, token);
  writeCookie(token);
}

export function clearToken(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(TOKEN_KEY);
  writeCookie(null);
}
