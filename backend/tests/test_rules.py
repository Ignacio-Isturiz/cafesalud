from app.expert_system.engine.evaluator import RuleEvaluator
from app.expert_system.engine.models import Condition, Rule


def test_rule_evaluation_matches_weighted_conditions() -> None:
    rule = Rule("demo", "disease", (Condition("part", "leaf", "Hoja", 2, True), Condition("spots", True, "Manchas", 3)))
    result = RuleEvaluator().evaluate(rule, {"part": "leaf", "spots": True})
    assert result.score == 100
    assert len(result.matched) == 2


def test_required_condition_rejects_rule() -> None:
    rule = Rule("demo", "disease", (Condition("part", "leaf", "Hoja", 2, True), Condition("spots", True, "Manchas", 3)))
    result = RuleEvaluator().evaluate(rule, {"part": "fruit", "spots": True})
    assert result.rejected is True
    assert result.score == 0

