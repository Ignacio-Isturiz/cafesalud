import { AlertTriangle, ArrowRight, BadgeCheck, RotateCcw } from "lucide-react";

import { EvidenceList } from "@/features/diagnosis/components/evidence-list";
import { RecommendationCard } from "@/features/diagnosis/components/recommendation-card";
import type { DiagnosisResponse } from "@/types/diagnosis";

const levelLabels = { low: "Bajo", medium: "Medio", high: "Alto" } as const;

export function DiagnosisResult({ result, onRestart }: { result: DiagnosisResponse; onRestart: () => void }) {
  const hypothesis = result.primary_hypothesis;
  return (
    <div className="diagnosis-result">
      <section className={hypothesis ? "result-summary" : "result-summary no-match"}>
        <span className="result-icon">{hypothesis ? <BadgeCheck /> : <AlertTriangle />}</span>
        <p className="result-eyebrow">{hypothesis ? "Posible diagnóstico" : "Resultado no concluyente"}</p>
        <h2>{hypothesis?.name ?? "No se encontró una hipótesis suficiente"}</h2>
        {hypothesis ? (
          <div className="score-row">
            <div><strong>{hypothesis.score}</strong><small>/ 100</small><span>Puntuación de compatibilidad</span></div>
            <div className={`compatibility ${hypothesis.compatibility}`}><small>Nivel</small><strong>{levelLabels[hypothesis.compatibility]}</strong></div>
          </div>
        ) : <p className="no-match-copy">Las respuestas no alcanzan el umbral mínimo de las reglas disponibles. Esto no descarta otros problemas del cultivo.</p>}
        <p className="score-note">La puntuación expresa coincidencia con reglas del sistema y no representa una probabilidad científica.</p>
      </section>

      <div className="result-content">
        <EvidenceList evidence={result.matched_evidence} />
        {result.explanation.length > 0 && (
          <section className="result-section reasoning-section">
            <h3>Explicación del razonamiento</h3>
            {result.explanation.map((text) => <p key={text}>{text}</p>)}
          </section>
        )}
        {result.alternative_hypotheses.length > 0 && (
          <section className="result-section">
            <h3>Hipótesis alternativas</h3>
            <div className="alternative-list">
              {result.alternative_hypotheses.map((item) => (
                <div key={item.disease}><div><strong>{item.name}</strong><small>Nivel {levelLabels[item.compatibility].toLowerCase()}</small></div><span>{item.score}/100</span></div>
              ))}
            </div>
          </section>
        )}
        <section className="result-section recommendations-section">
          <h3>Recomendaciones</h3>
          <ul>{result.recommendations.map((text, index) => <RecommendationCard index={index} key={text} text={text} />)}</ul>
        </section>
        <aside className="diagnosis-disclaimer"><AlertTriangle /><p><strong>Diagnóstico preliminar</strong>{result.disclaimer}</p></aside>
        <button className="secondary-button restart-button" onClick={onRestart} type="button"><RotateCcw /> Iniciar un nuevo diagnóstico <ArrowRight /></button>
      </div>
    </div>
  );
}
