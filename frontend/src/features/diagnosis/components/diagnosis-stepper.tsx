import { Check } from "lucide-react";

import type { DiagnosisStage } from "@/features/diagnosis/hooks/use-diagnosis";

const steps = [
  { id: "selection", label: "Parte afectada" },
  { id: "questions", label: "Síntomas" },
  { id: "review", label: "Revisión" },
  { id: "result", label: "Resultado" },
] as const;

const stagePosition: Record<DiagnosisStage, number> = {
  selection: 0,
  questions: 1,
  review: 2,
  analyzing: 3,
  result: 3,
};

export function DiagnosisStepper({ stage }: { stage: DiagnosisStage }) {
  const position = stagePosition[stage];
  return (
    <ol className="diagnosis-stepper" aria-label="Progreso del diagnóstico">
      {steps.map((step, index) => (
        <li className={index === position ? "active" : index < position ? "complete" : ""} key={step.id}>
          <span>{index < position ? <Check /> : index + 1}</span>
          <small>{step.label}</small>
        </li>
      ))}
    </ol>
  );
}
