import type { AnalysisResult } from "../types";

export async function analyzeDataset(file: File): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/analyze_dataset/", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Error al analizar el archivo");

  const data = await res.json();

  return data;
}
