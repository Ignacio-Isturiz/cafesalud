export type PlantPart = "leaf" | "stem" | "fruit";
export type QuestionType = "boolean" | "single_choice" | "multiple_choice" | "select";
export type AnswerValue = boolean | string | string[];

export interface QuestionOption {
  value: boolean | string;
  label: string;
  description?: string | null;
}

export interface ConditionalPredicate {
  question_key: string;
  operator: "equals" | "not_equals" | "contains";
  value: boolean | string;
}

export interface ConditionalGroup {
  all?: ConditionalPredicate[];
  any?: ConditionalPredicate[];
}

export type ConditionalLogic = ConditionalPredicate | ConditionalGroup;

export interface DiagnosisQuestion {
  id: string;
  key: string;
  label: string;
  description?: string | null;
  type: QuestionType;
  options: QuestionOption[];
  required: boolean;
  order: number;
  affected_part: PlantPart;
  conditional_logic?: ConditionalLogic | null;
  image?: string | null;
}

export interface Hypothesis {
  disease: string;
  name: string;
  score: number;
  compatibility: "low" | "medium" | "high";
}

export interface DiagnosisResponse {
  primary_hypothesis: Hypothesis | null;
  alternative_hypotheses: Hypothesis[];
  matched_evidence: { symptom: string; label: string }[];
  explanation: string[];
  recommendations: string[];
  disclaimer: string;
}
