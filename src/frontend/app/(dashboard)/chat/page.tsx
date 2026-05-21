"use client";

import { useMemo } from "react";
import { Trash2 } from "lucide-react";
import { PageHeader } from "@/components/common";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { Composer } from "@/components/chat/Composer";
import { Button } from "@/components/ui/button";
import { useChat } from "@/hooks/useChat";

function ensureSessionId() {
  if (typeof window === "undefined") return "default";
  const KEY = "pathpilot.chatSession";
  let id = window.localStorage.getItem(KEY);
  if (!id) {
    id = `s_${Math.random().toString(36).slice(2, 10)}`;
    window.localStorage.setItem(KEY, id);
  }
  return id;
}

const SUGGESTIONS = [
  "What skills should I focus on to become a Senior ML Engineer?",
  "Summarize the gaps in my current résumé.",
  "Generate a 4-week study plan for system design.",
  "Which projects would best showcase my skills?",
];

export default function ChatPage() {
  const sessionId = useMemo(ensureSessionId, []);
  const { messages, send, sending, reset } = useChat(sessionId);

  return (
    <div className="flex h-[calc(100vh-7rem)] flex-col">
      <PageHeader
        title="AI career coach"
        description="Grounded in your résumé and roadmap via local RAG over ChromaDB."
        actions={
          messages.length > 0 ? (
            <Button variant="ghost" size="sm" onClick={reset}>
              <Trash2 className="h-3.5 w-3.5" />
              Clear
            </Button>
          ) : null
        }
      />

      {messages.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center text-center">
          <h2 className="text-2xl font-semibold tracking-tight">How can I help today?</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Ask anything about your skills, gaps, or career path.
          </p>
          <div className="mt-6 grid w-full max-w-2xl gap-2 sm:grid-cols-2">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => void send(s)}
                className="rounded-xl border border-border bg-card/60 p-3 text-left text-sm text-muted-foreground transition hover:border-primary/40 hover:bg-card hover:text-foreground"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <ChatWindow messages={messages} pending={sending} />
      )}

      <div className="pt-3">
        <Composer onSend={send} disabled={sending} />
      </div>
    </div>
  );
}
