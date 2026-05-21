"use client";
import { useDropzone } from "react-dropzone";

export function Dropzone({ onFile }: { onFile: (file: File) => void }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    onDrop: (files) => files[0] && onFile(files[0]),
  });
  return (
    <div {...getRootProps()} className="cursor-pointer rounded border-2 border-dashed p-8 text-center">
      <input {...getInputProps()} />
      {isDragActive ? "Drop the PDF here" : "Drag & drop a PDF, or click to choose"}
    </div>
  );
}
