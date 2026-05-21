import axios, { AxiosError } from "axios";
import { API_BASE_URL } from "./env";
import { getToken, clearToken } from "./auth";

export interface ApiErrorPayload {
  message: string;
  code: string;
  details?: unknown;
}

export class ApiError extends Error {
  status: number;
  code: string;
  details?: unknown;

  constructor(payload: ApiErrorPayload, status: number) {
    super(payload.message);
    this.name = "ApiError";
    this.status = status;
    this.code = payload.code;
    this.details = payload.details;
  }
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30_000,
});

apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

apiClient.interceptors.response.use(
  (r) => r,
  (error: AxiosError<{ error?: ApiErrorPayload }>) => {
    const status = error.response?.status ?? 0;
    if (status === 401) clearToken();
    const payload = error.response?.data?.error ?? {
      message: error.message || "Request failed",
      code: "network_error",
    };
    return Promise.reject(new ApiError(payload, status));
  },
);
