"use client";

import { useMemo, useState } from "react";

import { diagnosisService } from "@/features/diagnosis/services/diagnosis.service";
import { getVisibleQuestions, hasAnswer, pruneHiddenAnswers, type DiagnosisAnswers } from "@/features/diagnosis/utils/questions";
import type { AnswerValue, DiagnosisQuestion, DiagnosisResponse, PlantPart } from "@/types/diagnosis";

export type DiagnosisStage = "selection" | "questions" | "review" | "analyzing" | "result";

export function useDiagnosis() {
  const [selectedPart, setSelectedPart] = useState<PlantPart | null>(null);
  const [questions, setQuestions] = useState<DiagnosisQuestion[]>([]);
  const [answers, setAnswers] = useState<DiagnosisAnswers>({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [stage, setStage] = useState<DiagnosisStage>("selection");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnosisResponse | null>(null);

  const visibleQuestions = useMemo(() => getVisibleQuestions(questions, answers), [answers, questions]);
  const currentQuestion = visibleQuestions[currentIndex];
  const progress = visibleQuestions.length === 0 ? 0 : ((currentIndex + 1) / visibleQuestions.length) * 100;

  function choosePart(part: PlantPart) {
    setSelectedPart(part);
    setError(null);
  }

  async function startQuestions() {
    if (!selectedPart) return;
    setLoading(true);
    setError(null);
    try {
      const catalog = await diagnosisService.getQuestions(selectedPart);
      if (catalog.length === 0) throw new Error("No encontramos preguntas para la parte seleccionada.");
      setQuestions(catalog.sort((a, b) => a.order - b.order));
      setAnswers({});
      setCurrentIndex(0);
      setStage("questions");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No fue posible cargar las preguntas.");
    } finally {
      setLoading(false);
    }
  }

  function setAnswer(questionKey: string, value: AnswerValue) {
    setAnswers((previous) => pruneHiddenAnswers(questions, { ...previous, [questionKey]: value }));
    setValidationError(null);
  }

  function nextQuestion() {
    if (!currentQuestion || !hasAnswer(currentQuestion, answers[currentQuestion.key])) {
      setValidationError("Selecciona una respuesta para continuar.");
      return;
    }
    setValidationError(null);
    if (currentIndex >= visibleQuestions.length - 1) {
      setStage("review");
      return;
    }
    setCurrentIndex((index) => index + 1);
  }

  function previousQuestion() {
    setValidationError(null);
    if (currentIndex === 0) {
      setStage("selection");
      return;
    }
    setCurrentIndex((index) => index - 1);
  }

  function editQuestion(questionKey: string) {
    const index = visibleQuestions.findIndex((question) => question.key === questionKey);
    setCurrentIndex(Math.max(index, 0));
    setStage("questions");
  }

  async function evaluate() {
    if (!selectedPart) return;
    setStage("analyzing");
    setError(null);
    try {
      const diagnosis = await diagnosisService.evaluate({ affected_part: selectedPart, ...answers });
      setResult(diagnosis);
      setStage("result");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No fue posible analizar las respuestas.");
      setStage("review");
    }
  }

  function restart() {
    setSelectedPart(null);
    setQuestions([]);
    setAnswers({});
    setCurrentIndex(0);
    setResult(null);
    setError(null);
    setValidationError(null);
    setStage("selection");
  }

  return {
    selectedPart,
    questions,
    visibleQuestions,
    currentQuestion,
    currentIndex,
    answers,
    progress,
    stage,
    loading,
    error,
    validationError,
    result,
    choosePart,
    startQuestions,
    setAnswer,
    nextQuestion,
    previousQuestion,
    editQuestion,
    evaluate,
    restart,
  };
}
