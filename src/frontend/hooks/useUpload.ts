"use client";
import { useState } from "react";
import { uploadService } from "@/services/upload.service";

export function useUpload() {
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);

  async function upload(file: File) {
    setUploading(true);
    setProgress(0);
    try {
      return await uploadService.upload(file, setProgress);
    } finally {
      setUploading(false);
    }
  }

  return { upload, progress, uploading };
}
