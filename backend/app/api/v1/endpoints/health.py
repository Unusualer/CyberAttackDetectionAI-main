from fastapi import APIRouter, Depends
from ....services.health import HealthCheckService
from ....api import deps

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}

@router.get("/health/detailed")
async def detailed_health_check(
    current_user = Depends(deps.get_current_active_superuser)
):
    """Detailed system health check"""
    health_service = HealthCheckService()
    return await health_service.check_all() 