from app.expert_system.engine.models import Rule, RuleEvaluation


class RuleEvaluator:
    def evaluate(self, rule: Rule, facts: dict[str, object]) -> RuleEvaluation:
        matched = tuple(condition for condition in rule.conditions if condition.matches(facts))
        missing = tuple(condition for condition in rule.conditions if not condition.matches(facts))
        rejected = any(condition.required for condition in missing)
        total_weight = sum(condition.weight for condition in rule.conditions)
        matched_weight = sum(condition.weight for condition in matched)
        score = 0.0 if rejected or total_weight == 0 else matched_weight / total_weight * 100
        return RuleEvaluation(rule.id, rule.disease_id, score, matched, missing, rejected)

