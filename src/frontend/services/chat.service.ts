import { apiClient } from "@/lib/api-client";
import type { ChatMessage } from "@/types/chat";

export const chatService = {
  send: (sessionId: string, message: string) =>
    apiClient.post<{ reply: ChatMessage }>("/chat", { sessionId, message }).then((r) => r.data),
  history: (sessionId: string) =>
    apiClient.get<ChatMessage[]>(`/chat/${sessionId}`).then((r) => r.data),
};
