"use client";

import { useState } from "react";
import { chatService } from "@/services/chat.service";
import { ApiError } from "@/lib/api-client";
import type { ChatMessage } from "@/types/chat";

function uid() {
  return Math.random().toString(36).slice(2);
}

export function useChat(sessionId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function send(content: string) {
    setError(null);
    const userMsg: ChatMessage = {
      id: uid(),
      role: "user",
      content,
      createdAt: new Date().toISOString(),
    };
    setMessages((m) => [...m, userMsg]);
    setSending(true);
    try {
      const { reply } = await chatService.send(sessionId, content);
      setMessages((m) => [
        ...m,
        { ...reply, id: reply.id || uid(), createdAt: reply.createdAt || new Date().toISOString() },
      ]);
      return reply;
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Failed to reach the AI";
      setError(msg);
      setMessages((m) => [
        ...m,
        {
          id: uid(),
          role: "system",
          content: `⚠️ ${msg}`,
          createdAt: new Date().toISOString(),
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  function reset() {
    setMessages([]);
    setError(null);
  }

  return { messages, send, sending, error, reset };
}
