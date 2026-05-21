"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, CheckCircle2, FileText } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/common";
import { Dropzone } from "@/components/upload/Dropzone";
import { UploadProgress } from "@/components/upload/UploadProgress";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useUpload } from "@/hooks/useUpload";
import { ApiError } from "@/lib/api-client";

const DOC_KEY = "pathpilot.lastDocId";

export default function UploadPage() {
  const router = useRouter();
  const { upload, uploading, progress } = useUpload();
  const [file, setFile] = useState<File | null>(null);
  const [docId, setDocId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload(f: File) {
    setError(null);
    setFile(f);
    setDocId(null);
    try {
      const { documentId } = await upload(f);
      setDocId(documentId);
      window.localStorage.setItem(DOC_KEY, documentId);
      toast.success("Document indexed");
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Upload failed";
      setError(msg);
      toast.error(msg);
    }
  }

  return (
    <>
      <PageHeader
        title="Upload résumé"
        description="PDF résumés are parsed, chunked, embedded with sentence-transformers, and stored in ChromaDB."
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2 space-y-4">
          <Dropzone onFile={handleUpload} />
          {file && (
            <div className="flex items-center gap-3 rounded-lg border border-border bg-muted/40 p-3 text-sm">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <div className="flex-1 truncate">
                <div className="font-medium truncate">{file.name}</div>
                <div className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} KB
                </div>
              </div>
              {docId && <CheckCircle2 className="h-4 w-4 text-emerald-500" />}
            </div>
          )}
          {uploading && <UploadProgress value={progress} />}
          {error && (
            <p role="alert" className="text-xs text-destructive">{error}</p>
          )}
          {docId && (
            <div className="flex flex-col gap-3 rounded-xl border border-border bg-accent/30 p-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="text-sm font-medium">Ready for analysis</div>
                <div className="text-xs text-muted-foreground">Continue to extract skills.</div>
              </div>
              <Button onClick={() => router.push("/skills")}>
                Analyze skills <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          )}
        </Card>

        <Card>
          <h3 className="text-sm font-semibold">How it works</h3>
          <ol className="mt-3 space-y-3 text-sm text-muted-foreground">
            <li><span className="font-medium text-foreground">1.</span> PDF → text via pypdf</li>
            <li><span className="font-medium text-foreground">2.</span> Recursive chunking</li>
            <li><span className="font-medium text-foreground">3.</span> Embed (sentence-transformers)</li>
            <li><span className="font-medium text-foreground">4.</span> Persist to ChromaDB</li>
            <li><span className="font-medium text-foreground">5.</span> Available to RAG + LangGraph</li>
          </ol>
        </Card>
      </div>
    </>
  );
}
