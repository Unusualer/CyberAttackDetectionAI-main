from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Any
from datetime import datetime

class ReportType(str, Enum):
    THREAT_SUMMARY = "threat_summary"
    ML_PERFORMANCE = "ml_performance"
    SYSTEM_HEALTH = "system_health"

class Report(BaseModel):
    id: str
    organization_id: str
    report_type: ReportType
    start_date: datetime
    end_date: datetime
    data: Dict[str, Any]
    insights: List[Dict[str, Any]]
    visualizations: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    generated_at: datetime 