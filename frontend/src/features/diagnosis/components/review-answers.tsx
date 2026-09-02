import { ArrowLeft, Pencil, SearchCheck } from "lucide-react";

import { formatAnswer, type DiagnosisAnswers } from "@/features/diagnosis/utils/questions";
import type { DiagnosisQuestion } from "@/types/diagnosis";

interface ReviewAnswersProps {
  questions: DiagnosisQuestion[];
  answers: DiagnosisAnswers;
  error: string | null;
  onBack: () => void;
  onEdit: (key: string) => void;
  onEvaluate: () => void;
}

export function ReviewAnswers({ questions, answers, error, onBack, onEdit, onEvaluate }: ReviewAnswersProps) {
  return (
    <article className="review-card">
      <div className="review-heading">
        <span><SearchCheck /></span>
        <div><p>Antes de analizar</p><h2>Revisa tus respuestas</h2><small>Puedes corregir cualquier observación antes de consultar el sistema experto.</small></div>
      </div>
      <div className="answer-list">
        {questions.map((question, index) => (
          <div className="answer-row" key={question.key}>
            <span>{index + 1}</span>
            <div><strong>{question.label}</strong><p>{formatAnswer(question, answers[question.key])}</p></div>
            <button aria-label={`Editar: ${question.label}`} onClick={() => onEdit(question.key)} type="button"><Pencil /></button>
          </div>
        ))}
      </div>
      {error && <p className="diagnosis-error" role="alert">{error}</p>}
      <div className="question-actions">
        <button className="text-button" onClick={onBack} type="button"><ArrowLeft /> Volver</button>
        <button className="primary-button" onClick={onEvaluate} type="button"><SearchCheck /> Analizar diagnóstico</button>
      </div>
    </article>
  );
}
