from app.domain.disease import DiseaseDefinition
from app.expert_system.knowledge.catalog import DISEASES, DISEASE_BY_ID


class KnowledgeDiseaseRepository:
    """Read-only repository for versioned, reviewable expert knowledge."""

    def list(self) -> tuple[DiseaseDefinition, ...]:
        return DISEASES

    def get(self, disease_id: str) -> DiseaseDefinition | None:
        return DISEASE_BY_ID.get(disease_id)

