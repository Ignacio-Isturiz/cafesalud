import type { DiagnosisResponse } from "@/types/diagnosis";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) throw new Error(`API request failed with ${response.status}`);
  return response.json() as Promise<T>;
}

export const diagnosisApi = {
  evaluate: (answers: Record<string, unknown>) =>
    request<DiagnosisResponse>("/diagnosis/evaluate", {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
};

