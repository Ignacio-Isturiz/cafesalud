from fastapi import APIRouter

from app.api.v1.routes import diagnosis, diseases, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(diseases.router, prefix="/diseases", tags=["diseases"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])

