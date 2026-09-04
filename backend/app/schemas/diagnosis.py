from typing import Any, Literal

from pydantic import BaseModel, Field


class DiagnosisRequest(BaseModel):
    answers: dict[str, Any] = Field(min_length=1)


class Hypothesis(BaseModel):
    disease: str
    name: str
    score: int = Field(ge=0, le=100, description="Puntuación de coincidencia; no es una probabilidad científica.")
    compatibility: Literal["low", "medium", "high"]


class Evidence(BaseModel):
    symptom: str
    label: str


class DiagnosisResponse(BaseModel):
    primary_hypothesis: Hypothesis | None
    alternative_hypotheses: list[Hypothesis]
    matched_evidence: list[Evidence]
    explanation: list[str]
    recommendations: list[str]
    disclaimer: str


class QuestionOption(BaseModel):
    value: str | bool
    label: str
    description: str | None = None


class ConditionalPredicate(BaseModel):
    question_key: str
    operator: Literal["equals", "not_equals", "contains"]
    value: str | bool


class ConditionalGroup(BaseModel):
    all: list[ConditionalPredicate] | None = None
    any: list[ConditionalPredicate] | None = None


class QuestionRead(BaseModel):
    id: str
    key: str
    label: str
    description: str | None = None
    type: Literal["boolean", "single_choice", "multiple_choice", "select"]
    options: list[QuestionOption]
    required: bool
    order: int
    affected_part: Literal["leaf", "stem", "fruit"]
    conditional_logic: ConditionalPredicate | ConditionalGroup | None = None
    image: str | None = None
