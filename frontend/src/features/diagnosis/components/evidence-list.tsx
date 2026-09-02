import { CheckCircle2 } from "lucide-react";

import type { DiagnosisResponse } from "@/types/diagnosis";

export function EvidenceList({ evidence }: { evidence: DiagnosisResponse["matched_evidence"] }) {
  if (evidence.length === 0) return null;
  return (
    <section className="result-section">
      <h3>Evidencias coincidentes</h3>
      <ul className="evidence-list">
        {evidence.map((item) => <li key={item.symptom}><CheckCircle2 /><span>{item.label}</span></li>)}
      </ul>
    </section>
  );
}
