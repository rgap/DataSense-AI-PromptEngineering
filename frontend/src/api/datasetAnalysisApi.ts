import type { AnalysisResult } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function analyzeDataset(file: File): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/analyze_dataset/`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Error al analizar el archivo");

  const data = await res.json();

  return data;
}
