from typing import Literal

from fastapi import APIRouter, Query

from app.expert_system.knowledge.questions import questions_for
from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse, QuestionRead
from app.services.diagnosis_service import DiagnosisService

router = APIRouter()
service = DiagnosisService()


@router.get("/questions", response_model=list[QuestionRead])
def list_questions(
    affected_part: Literal["leaf", "stem", "stem_branch", "fruit"] | None = Query(default=None),
) -> tuple[dict[str, object], ...]:
    return questions_for(affected_part)


@router.post("/evaluate", response_model=DiagnosisResponse)
def evaluate_diagnosis(request: DiagnosisRequest) -> dict[str, object]:
    return service.evaluate(request.answers)
