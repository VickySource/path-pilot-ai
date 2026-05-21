"use client";

import { useRef, useState } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export function Composer({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void | Promise<void>;
  disabled?: boolean;
}) {
  const [text, setText] = useState("");
  const taRef = useRef<HTMLTextAreaElement>(null);

  function submit() {
    const value = text.trim();
    if (!value || disabled) return;
    setText("");
    void onSend(value);
    requestAnimationFrame(() => taRef.current?.focus());
  }

  return (
    <form
      className="relative rounded-2xl border border-border bg-card/80 p-2 shadow-sm backdrop-blur transition focus-within:border-primary/40"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
    >
      <Textarea
        ref={taRef}
        rows={1}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ask about your skills, roadmap, or next role…"
        className="min-h-[44px] resize-none border-0 bg-transparent px-2 py-2 shadow-none focus-visible:ring-0"
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submit();
          }
        }}
      />
      <div className="flex items-center justify-between px-1 pt-1 pb-1">
        <span className="text-[10px] text-muted-foreground">⏎ to send · Shift+⏎ for newline</span>
        <Button size="sm" type="submit" disabled={disabled || !text.trim()} className="rounded-full px-3">
          <ArrowUp className="h-3.5 w-3.5" />
          Send
        </Button>
      </div>
    </form>
  );
}
