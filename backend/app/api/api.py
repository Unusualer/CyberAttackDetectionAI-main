from fastapi import APIRouter
from app.api.endpoints import threat_detection

api_router = APIRouter()
api_router.include_router(
    threat_detection.router,
    prefix="/threat-detection",
    tags=["threat-detection"]
) 