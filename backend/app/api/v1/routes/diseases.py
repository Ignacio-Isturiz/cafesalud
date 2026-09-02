from fastapi import APIRouter, HTTPException

from app.repositories.disease_repository import KnowledgeDiseaseRepository
from app.schemas.disease import DiseaseRead

router = APIRouter()
repository = KnowledgeDiseaseRepository()


@router.get("", response_model=list[DiseaseRead])
def list_diseases() -> tuple[object, ...]:
    return repository.list()


@router.get("/{disease_id}", response_model=DiseaseRead)
def get_disease(disease_id: str) -> object:
    disease = repository.get(disease_id)
    if disease is None:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

