from typing import Any

from app.expert_system.engine.answer_normalizer import AnswerNormalizer
from app.expert_system.engine.evaluator import RuleEvaluator
from app.expert_system.explanations.builder import ExplanationBuilder
from app.expert_system.knowledge.catalog import DISEASE_BY_ID
from app.expert_system.knowledge.rules import RULES
from app.expert_system.scoring.ranker import ScoreRanker


class InferenceEngine:
    minimum_score = 25

    def __init__(self) -> None:
        self.evaluator = RuleEvaluator()
        self.ranker = ScoreRanker()
        self.explanations = ExplanationBuilder()
        self.normalizer = AnswerNormalizer()

    def evaluate(self, raw_facts: dict[str, Any]) -> dict[str, Any]:
        facts = self.normalizer.normalize(raw_facts)
        evaluations = [self.evaluator.evaluate(rule, facts) for rule in RULES]
        ranked = [match for match in self.ranker.rank(evaluations) if match.score >= self.minimum_score]

        hypotheses = [self._hypothesis(match) for match in ranked]
        primary = hypotheses[0] if hypotheses else None
        alternatives = hypotheses[1:3]

        primary_match = ranked[0] if ranked else None
        matched_conditions = [] if primary_match is None else [
            condition
            for evaluation in primary_match.evaluations
            for condition in evaluation.matched
            if not condition.required
        ]
        unique_conditions = {condition.field: condition for condition in matched_conditions}
        disease = DISEASE_BY_ID.get(primary_match.disease_id) if primary_match else None

        return {
            "primary_hypothesis": primary,
            "alternative_hypotheses": alternatives,
            "matched_evidence": [
                {"symptom": condition.field, "label": condition.label}
                for condition in unique_conditions.values()
            ],
            "explanation": [] if primary_match is None else self.explanations.build(primary_match.evaluations),
            "recommendations": list(disease.recommendations) if disease else [
                "Registra los síntomas observados y consulta a un profesional agrónomo."
            ],
            "disclaimer": "Este resultado corresponde a una orientación diagnóstica preliminar y no reemplaza la evaluación de un profesional agrónomo.",
        }

    @staticmethod
    def _compatibility(score: int) -> str:
        if score >= 75:
            return "high"
        if score >= 50:
            return "medium"
        return "low"

    def _hypothesis(self, match: object) -> dict[str, Any]:
        disease = DISEASE_BY_ID[match.disease_id]
        return {
            "disease": disease.id,
            "name": disease.name,
            "score": match.score,
            "compatibility": self._compatibility(match.score),
        }
