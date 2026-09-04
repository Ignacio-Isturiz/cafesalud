import type { AnswerValue, ConditionalPredicate, DiagnosisQuestion, QuestionOption } from "@/types/diagnosis";

export type DiagnosisAnswers = Record<string, AnswerValue>;

function matchesPredicate(condition: ConditionalPredicate, answers: DiagnosisAnswers): boolean {
  const answer = answers[condition.question_key];
  if (answer === undefined) return false;
  if (condition.operator === "equals") return answer === condition.value;
  if (condition.operator === "not_equals") return answer !== condition.value;
  return Array.isArray(answer) && answer.includes(String(condition.value));
}

function matchesCondition(question: DiagnosisQuestion, answers: DiagnosisAnswers): boolean {
  const logic = question.conditional_logic;
  if (!logic) return true;
  if ("question_key" in logic) return matchesPredicate(logic, answers);

  const allMatch = !logic.all || logic.all.every((condition) => matchesPredicate(condition, answers));
  const anyMatch = !logic.any || logic.any.some((condition) => matchesPredicate(condition, answers));
  return allMatch && anyMatch;
}

export function getVisibleQuestions(questions: DiagnosisQuestion[], answers: DiagnosisAnswers) {
  return questions.filter((question) => matchesCondition(question, answers));
}

export function pruneHiddenAnswers(questions: DiagnosisQuestion[], answers: DiagnosisAnswers) {
  let next = { ...answers };
  let changed = true;

  while (changed) {
    const visibleKeys = new Set(getVisibleQuestions(questions, next).map((question) => question.key));
    const entries = Object.entries(next).filter(([key]) => visibleKeys.has(key));
    changed = entries.length !== Object.keys(next).length;
    next = Object.fromEntries(entries);
  }
  return next;
}

export function hasAnswer(question: DiagnosisQuestion, answer: AnswerValue | undefined) {
  if (!question.required) return true;
  if (Array.isArray(answer)) return answer.length > 0;
  return answer !== undefined && answer !== "";
}

export function getOptionLabel(options: QuestionOption[], value: string | boolean) {
  return options.find((option) => option.value === value)?.label ?? String(value);
}

export function formatAnswer(question: DiagnosisQuestion, answer: AnswerValue | undefined) {
  if (answer === undefined) return "Sin respuesta";
  if (Array.isArray(answer)) return answer.map((value) => getOptionLabel(question.options, value)).join(", ");
  return getOptionLabel(question.options, answer);
}
