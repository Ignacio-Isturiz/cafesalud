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
            if condition.field != "affected_part" and condition.expected is not False
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
            "recommendations": list(disease.recommendations) if disease else self._no_match_guidance(facts),
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

    @staticmethod
    def _no_match_guidance(facts: dict[str, Any]) -> list[str]:
        if facts.get("affected_part") == "leaf" and facts.get("leaf_lesions") is False:
            if facts.get("foliar_decline") is True:
                return [
                    "El patrón no coincide con las tres enfermedades foliares evaluadas; analiza otras causas de amarillamiento, marchitez o caída de hojas con un profesional agrónomo.",
                    "Registra las condiciones del cultivo y la evolución de los síntomas.",
                ]
            return [
                "No se observó un patrón compatible con las enfermedades foliares seleccionadas.",
                "Continúa vigilando la planta y consulta a un profesional si aparecen nuevos síntomas.",
            ]
        if facts.get("affected_part") == "leaf":
            return [
                "Las lesiones no coinciden con los patrones de mancha de hierro, roya u ojo de gallo evaluados.",
                "Documenta los síntomas y consulta a un profesional agrónomo para analizar otras causas foliares.",
            ]
        if facts.get("affected_part") == "stem_branch":
            return [
                "No se observó un patrón compatible con las afecciones de tallo o rama evaluadas.",
                "Continúa vigilando la planta y consulta a un profesional si aparecen lesiones o secamiento progresivo.",
            ]
        if facts.get("affected_part") == "fruit":
            return [
                "No se observó un patrón compatible con las afecciones del fruto evaluadas.",
                "Continúa vigilando la planta y consulta a un profesional si aparecen lesiones, caída, cambios de color o desarrollo anormal.",
            ]
        return ["Registra los síntomas observados y consulta a un profesional agrónomo."]
