from app.expert_system.engine.models import RuleEvaluation


class ExplanationBuilder:
    def build(self, evaluations: tuple[RuleEvaluation, ...]) -> list[str]:
        evidence = []
        for evaluation in evaluations:
            evidence.extend(
                condition.label
                for condition in evaluation.matched
                if condition.field != "affected_part" and condition.expected is not False
            )
        unique = list(dict.fromkeys(evidence))
        if not unique:
            return []
        return [f"La orientación coincide con: {', '.join(unique).lower()}."]
