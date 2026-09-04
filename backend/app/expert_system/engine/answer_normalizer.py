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
        self._derive_stem_facts(facts)
        self._derive_fruit_facts(facts)
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
        if "iron_spot_compatible" not in facts:
            facts["iron_spot_compatible"] = (
                facts["circular_brown_lesions"]
                and facts["light_center"]
                and facts["yellow_halo"]
            )
        if "eye_spot_compatible" not in facts:
            facts["eye_spot_compatible"] = (
                facts["target_like_lesions"]
                and facts["light_center"]
                and facts["dark_margin"]
            )
        if facts.get("recent_rains") is True:
            facts["humid_conditions"] = True

    @staticmethod
    def _derive_stem_facts(facts: dict[str, Any]) -> None:
        if "stem_path_active" not in facts:
            facts["stem_path_active"] = (
                facts.get("stem_lesions") is True
                or facts.get("stem_progressive_drying") is True
            )

    @staticmethod
    def _derive_fruit_facts(facts: dict[str, Any]) -> None:
        if "fruit_abnormal_change" not in facts:
            facts["fruit_abnormal_change"] = any(
                facts.get(key) is True
                for key in ("premature_fruit_drop", "fruit_color_change", "abnormal_fruit_development")
            )
        if "fruit_path_active" not in facts:
            facts["fruit_path_active"] = (
                facts.get("fruit_lesions") is True
                or facts.get("fruit_abnormal_change") is True
            )
