from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiseaseDefinition:
    id: str
    name: str
    description: str
    affected_part: str
    symptoms: tuple[str, ...]
    recommendations: tuple[str, ...]

