import { Sprout } from "lucide-react";

import { DiagnosisFlow } from "@/features/diagnosis/components/diagnosis-flow";

export default function DiagnosisPage() {
  return (
    <section className="diagnosis-page">
      <div className="diagnosis-hero"><span><Sprout /></span><p>Orientación preliminar</p><h1>Diagnóstico</h1><p>Selecciona la parte de la planta que presenta el problema.</p></div>
      <DiagnosisFlow />
    </section>
  );
}
