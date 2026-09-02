from typing import Any


class AnswerNormalizer:
    """Converts transport-friendly questionnaire answers into expert-system facts."""

    part_aliases = {
        "hoja": "leaf",
        "tallo": "stem_branch",
        "rama": "stem_branch",
        "stem": "stem_branch",
        "fruto": "fruit",
    }

    def normalize(self, raw_answers: dict[str, Any]) -> dict[str, Any]:
        facts = {
            key.strip().lower(): self._normalize_value(value)
            for key, value in raw_answers.items()
        }
        facts["affected_part"] = self.part_aliases.get(facts.get("affected_part"), facts.get("affected_part"))
        self._derive_leaf_facts(facts)
        return facts

    def _normalize_value(self, value: Any) -> Any:
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"sí", "si", "true", "yes"}:
                return True
            if lowered in {"no", "false"}:
                return False
            return self.part_aliases.get(lowered, lowered)
        if isinstance(value, list):
            return [self._normalize_value(item) for item in value]
        return value

    @staticmethod
    def _contains(value: Any, item: str) -> bool:
        return item in value if isinstance(value, list) else value == item

    def _derive_leaf_facts(self, facts: dict[str, Any]) -> None:
        colors = facts.get("lesion_color", [])
        borders = facts.get("lesion_border_halo", [])
        shape = facts.get("lesion_shape")

        if "yellow_spots" not in facts:
            facts["yellow_spots"] = self._contains(colors, "yellow")
        if "circular_brown_lesions" not in facts:
            facts["circular_brown_lesions"] = shape == "circular" and self._contains(colors, "brown")
        if "light_center" not in facts:
            facts["light_center"] = facts.get("lesion_center") == "light"
        if "yellow_halo" not in facts:
            facts["yellow_halo"] = self._contains(borders, "yellow") or self._contains(borders, "reddish")
        if "target_like_lesions" not in facts:
            facts["target_like_lesions"] = shape == "target_like" or facts.get("eye_spot_compatible") is True
        if "dark_margin" not in facts:
            facts["dark_margin"] = self._contains(borders, "dark")
        if facts.get("recent_rains") is True:
            facts["humid_conditions"] = True
