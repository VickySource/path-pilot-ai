"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { Sparkles } from "lucide-react";

export function ChatWindow({
  messages,
  pending,
}: {
  messages: ChatMessage[];
  pending?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: "smooth" });
  }, [messages.length, pending]);

  return (
    <div ref={ref} className="scrollbar-thin flex-1 space-y-4 overflow-y-auto px-1 py-4">
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      {pending && (
        <div className="flex gap-3 animate-fade-up">
          <span className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-primary to-accent-foreground text-primary-foreground">
            <Sparkles className="h-3.5 w-3.5" />
          </span>
          <div className="flex items-center gap-1 rounded-2xl rounded-bl-md border border-border bg-card px-4 py-3">
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground" />
          </div>
        </div>
      )}
    </div>
  );
}
