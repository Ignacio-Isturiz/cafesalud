import { ArrowLeft, ArrowRight, Info } from "lucide-react";
import Image from "next/image";

import { OptionCard } from "@/features/diagnosis/components/option-card";
import { ProgressBar } from "@/features/diagnosis/components/progress-bar";
import type { AnswerValue, DiagnosisQuestion } from "@/types/diagnosis";

interface QuestionCardProps {
  question: DiagnosisQuestion;
  answer?: AnswerValue;
  current: number;
  total: number;
  progress: number;
  validationError: string | null;
  isLast: boolean;
  onAnswer: (value: AnswerValue) => void;
  onBack: () => void;
  onNext: () => void;
}

export function QuestionCard({ question, answer, current, total, progress, validationError, isLast, onAnswer, onBack, onNext }: QuestionCardProps) {
  const multiple = question.type === "multiple_choice";

  function selectOption(value: boolean | string) {
    if (!multiple) {
      onAnswer(value);
      return;
    }
    const selected = Array.isArray(answer) ? answer : [];
    const stringValue = String(value);
    onAnswer(selected.includes(stringValue)
      ? selected.filter((item) => item !== stringValue)
      : [...selected, stringValue]);
  }

  return (
    <div className="question-shell">
      <ProgressBar current={current} total={total} value={progress} />
      <article className="question-card">
        {question.image && (
          <div className="question-image">
            <Image
              alt={`Ejemplo visual para responder: ${question.label}`}
              fill
              priority={current === 1}
              sizes="(max-width: 700px) calc(100vw - 70px), 636px"
              src={question.image}
            />
            <span>Ejemplo visual</span>
          </div>
        )}
        <div className="question-heading">
          <span>{String(current).padStart(2, "0")}</span>
          <div>
            <h2>{question.label}</h2>
            {question.description && <p><Info />{question.description}</p>}
          </div>
        </div>
        <div className={`option-grid ${question.options.length > 4 ? "compact" : ""}`}>
          {question.options.map((option) => {
            const selected = Array.isArray(answer)
              ? answer.includes(String(option.value))
              : answer === option.value;
            return <OptionCard key={String(option.value)} multiple={multiple} onSelect={() => selectOption(option.value)} option={option} selected={selected} />;
          })}
        </div>
        {validationError && <p className="validation-message" role="alert">{validationError}</p>}
        <div className="question-actions">
          <button className="text-button" onClick={onBack} type="button"><ArrowLeft /> Volver</button>
          <button className="primary-button" onClick={onNext} type="button">
            {isLast ? "Revisar respuestas" : "Siguiente"} <ArrowRight />
          </button>
        </div>
      </article>
    </div>
  );
}
