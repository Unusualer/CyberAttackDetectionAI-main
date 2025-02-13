from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from ....schemas.reports import Report, ReportType
from ....services.reporting import ReportingService
from ....api import deps
from ....core.security import get_current_active_user

router = APIRouter()

@router.get("/reports", response_model=List[Report])
async def get_reports(
    report_type: Optional[ReportType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(default=50, le=100),
    current_user = Depends(get_current_active_user)
):
    """Get security reports"""
    reporting = ReportingService()
    return await reporting.get_reports(
        organization_id=current_user.organization_id,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

@router.post("/reports/generate")
async def generate_report(
    report_type: ReportType,
    start_date: datetime,
    end_date: datetime,
    current_user = Depends(get_current_active_user)
):
    """Generate a new report"""
    reporting = ReportingService()
    return await reporting.generate_report(
        organization_id=current_user.organization_id,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/reports/{report_id}")
async def get_report(
    report_id: str,
    current_user = Depends(get_current_active_user)
):
    """Get a specific report"""
    reporting = ReportingService()
    return await reporting.get_report(
        report_id=report_id,
        organization_id=current_user.organization_id
    ) 