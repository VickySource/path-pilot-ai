import type { ChatMessage } from "@/types/chat";
import { cn } from "@/lib/utils";
import { Sparkles } from "lucide-react";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const mine = message.role === "user";
  return (
    <div
      className={cn(
        "flex w-full gap-3 animate-fade-up",
        mine ? "justify-end" : "justify-start",
      )}
    >
      {!mine && (
        <span className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-primary to-accent-foreground text-primary-foreground">
          <Sparkles className="h-3.5 w-3.5" />
        </span>
      )}
      <div
        className={cn(
          "max-w-[78%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm leading-relaxed shadow-sm",
          mine
            ? "rounded-br-md bg-primary text-primary-foreground"
            : "rounded-bl-md bg-card text-card-foreground border border-border",
        )}
      >
        {message.content}
      </div>
    </div>
  );
}
