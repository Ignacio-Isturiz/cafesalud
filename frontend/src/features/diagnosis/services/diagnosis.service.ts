import type { DiagnosisQuestion, DiagnosisResponse, PlantPart } from "@/types/diagnosis";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
  } catch {
    throw new Error("No pudimos conectar con el sistema experto. Comprueba que el backend esté disponible.");
  }

  if (!response.ok) {
    throw new Error(response.status >= 500
      ? "El sistema experto no está disponible en este momento. Inténtalo de nuevo."
      : "No fue posible completar la solicitud de diagnóstico.");
  }
  return response.json() as Promise<T>;
}

export const diagnosisService = {
  getQuestions: (affectedPart: PlantPart) =>
    request<DiagnosisQuestion[]>(`/diagnosis/questions?affected_part=${affectedPart}`),
  evaluate: (answers: Record<string, unknown>) =>
    request<DiagnosisResponse>("/diagnosis/evaluate", {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
};
