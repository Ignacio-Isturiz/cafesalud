"use client";

import { BrainCircuit, LoaderCircle } from "lucide-react";
import { useEffect, useRef } from "react";

import { DiagnosisResult } from "@/features/diagnosis/components/diagnosis-result";
import { DiagnosisStepper } from "@/features/diagnosis/components/diagnosis-stepper";
import { QuestionCard } from "@/features/diagnosis/components/question-card";
import { ReviewAnswers } from "@/features/diagnosis/components/review-answers";
import { useDiagnosis } from "@/features/diagnosis/hooks/use-diagnosis";
import { PlantPartSelector } from "@/features/diagnosis/plant-part-selector";

export function DiagnosisFlow() {
  const diagnosis = useDiagnosis();
  const flowRef = useRef<HTMLDivElement>(null);
  const firstRender = useRef(true);

  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    flowRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [diagnosis.currentIndex, diagnosis.stage]);

  return (
    <div className="diagnosis-flow" ref={flowRef}>
      <DiagnosisStepper stage={diagnosis.stage} />
      {diagnosis.stage === "selection" && (
        <PlantPartSelector
          error={diagnosis.error}
          loading={diagnosis.loading}
          onContinue={diagnosis.startQuestions}
          onSelect={diagnosis.choosePart}
          selected={diagnosis.selectedPart}
        />
      )}
      {diagnosis.stage === "questions" && diagnosis.currentQuestion && (
        <QuestionCard
          answer={diagnosis.answers[diagnosis.currentQuestion.key]}
          current={diagnosis.currentIndex + 1}
          isLast={diagnosis.currentIndex === diagnosis.visibleQuestions.length - 1}
          onAnswer={(value) => diagnosis.setAnswer(diagnosis.currentQuestion!.key, value)}
          onBack={diagnosis.previousQuestion}
          onNext={diagnosis.nextQuestion}
          progress={diagnosis.progress}
          question={diagnosis.currentQuestion}
          total={diagnosis.visibleQuestions.length}
          validationError={diagnosis.validationError}
        />
      )}
      {diagnosis.stage === "review" && (
        <ReviewAnswers
          answers={diagnosis.answers}
          error={diagnosis.error}
          onBack={() => diagnosis.editQuestion(diagnosis.visibleQuestions.at(-1)?.key ?? "")}
          onEdit={diagnosis.editQuestion}
          onEvaluate={diagnosis.evaluate}
          questions={diagnosis.visibleQuestions}
        />
      )}
      {diagnosis.stage === "analyzing" && (
        <div className="analysis-card" role="status">
          <span><BrainCircuit /><LoaderCircle className="spin" /></span>
          <h2>Analizando tus respuestas</h2>
          <p>El sistema experto compara las evidencias con sus reglas de conocimiento.</p>
        </div>
      )}
      {diagnosis.stage === "result" && diagnosis.result && <DiagnosisResult onRestart={diagnosis.restart} result={diagnosis.result} />}
    </div>
  );
}
