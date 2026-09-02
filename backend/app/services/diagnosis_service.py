from typing import Any

from app.expert_system import InferenceEngine


class DiagnosisService:
    def __init__(self, engine: InferenceEngine | None = None) -> None:
        self.engine = engine or InferenceEngine()

    def evaluate(self, answers: dict[str, Any]) -> dict[str, Any]:
        return self.engine.evaluate(answers)

