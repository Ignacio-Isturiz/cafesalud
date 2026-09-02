from dataclasses import dataclass

from app.expert_system.engine.models import RuleEvaluation


@dataclass(frozen=True, slots=True)
class RankedMatch:
    disease_id: str
    score: int
    evaluations: tuple[RuleEvaluation, ...]


class ScoreRanker:
    def rank(self, evaluations: list[RuleEvaluation]) -> list[RankedMatch]:
        grouped: dict[str, list[RuleEvaluation]] = {}
        for evaluation in evaluations:
            grouped.setdefault(evaluation.disease_id, []).append(evaluation)

        ranked = [
            RankedMatch(
                disease_id=disease_id,
                score=round(max(item.score for item in disease_evaluations)),
                evaluations=tuple(disease_evaluations),
            )
            for disease_id, disease_evaluations in grouped.items()
        ]
        return sorted(ranked, key=lambda match: match.score, reverse=True)

