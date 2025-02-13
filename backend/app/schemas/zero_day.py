from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ReconstructionAnalysis(BaseModel):
    autoencoder_diff: float = Field(..., description="Difference in autoencoder reconstruction")
    pca_diff: float = Field(..., description="Difference in PCA reconstruction")

class AnomalyScores(BaseModel):
    isolation_forest: float = Field(..., description="Anomaly score from Isolation Forest")
    autoencoder: float = Field(..., description="Anomaly score from Autoencoder")
    pca: float = Field(..., description="Anomaly score from PCA")

class DetectionDetails(BaseModel):
    feature_importance: Dict[str, float] = Field(
        ...,
        description="Importance score for each feature"
    )
    reconstruction_analysis: ReconstructionAnalysis
    timestamp: datetime

class ZeroDayDetection(BaseModel):
    is_zero_day: bool = Field(..., description="Whether a zero-day attack was detected")
    confidence: float = Field(
        ...,
        description="Confidence score of the detection",
        ge=0.0,
        le=1.0
    )
    anomaly_scores: AnomalyScores
    details: DetectionDetails

class ZeroDayAlert(BaseModel):
    alert_id: str = Field(..., description="Unique identifier for the alert")
    event_id: str = Field(..., description="ID of the triggering security event")
    detection_result: ZeroDayDetection
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(
        ...,
        description="Current status of the alert",
        regex="^(new|investigating|contained|resolved)$"
    )
    severity: str = Field(
        ...,
        description="Severity level of the alert",
        regex="^(low|medium|high|critical)$"
    )
    assigned_to: Optional[str] = Field(
        None,
        description="ID of the security analyst assigned to the alert"
    )
    resolution: Optional[str] = Field(
        None,
        description="Resolution details if the alert is resolved"
    )
    mitigation_steps: List[str] = Field(
        default_factory=list,
        description="Steps taken to mitigate the threat"
    )
    indicators: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Indicators of compromise"
    )

class ZeroDayStats(BaseModel):
    total_detections: int = Field(..., description="Total number of zero-day detections")
    high_confidence: int = Field(
        ...,
        description="Number of high confidence detections"
    )
    average_confidence: float = Field(
        ...,
        description="Average confidence score of detections",
        ge=0.0,
        le=1.0
    )
    detection_trend: str = Field(
        ...,
        description="Trend in detection rate",
        regex="^(increasing|decreasing|stable)$"
    )
    most_common_indicators: List[str] = Field(
        ...,
        description="Most frequently observed indicators"
    )
    time_distribution: Dict[str, int] = Field(
        ...,
        description="Distribution of detections over time"
    )
    false_positive_rate: Optional[float] = Field(
        None,
        description="Estimated false positive rate",
        ge=0.0,
        le=1.0
    )
    detection_by_type: Dict[str, int] = Field(
        ...,
        description="Number of detections by attack type"
    ) 