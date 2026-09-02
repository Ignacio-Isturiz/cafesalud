from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Condition:
    field: str
    expected: Any
    label: str
    weight: float = 1.0
    required: bool = False

    def matches(self, facts: dict[str, Any]) -> bool:
        actual = facts.get(self.field)
        if isinstance(self.expected, (tuple, list, set)):
            return actual in self.expected
        return actual == self.expected


@dataclass(frozen=True, slots=True)
class Rule:
    id: str
    disease_id: str
    conditions: tuple[Condition, ...]


@dataclass(frozen=True, slots=True)
class RuleEvaluation:
    rule_id: str
    disease_id: str
    score: float
    matched: tuple[Condition, ...]
    missing: tuple[Condition, ...]
    rejected: bool

